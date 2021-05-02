from globals import api, get_rand, get_month_start, session_factory
from libs.Handler import Handler
from libs.Picture import Picture

import datetime


def check_func(msg):
    text = msg.get('text')
    return text.startswith("Баян, топ месяца") or text.startswith("Баян, топ за месяц")


def process_func(msg):
    peer_id = msg.get('peer_id')
    local_session = session_factory()
    month_start_dt = get_month_start()
    pictures_from_month_start = Picture.get_all_from(month_start_dt, local_session, limit=10)
    attachment_strings = list(
        map(
            lambda x: x.get_api_string(peer_id),
            sorted(
                pictures_from_month_start,
                reverse=True,
                key=lambda pic: (pic.ups / pic.downs) * (pic.ups + pic.downs) if pic.downs > 0 else 0
            )
        )
    )
    local_session.close()
    api.messages.send(peer_id=peer_id,
                      message="Топ за месяц",
                      attachment=','.join(attachment_strings),
                      random_id=get_rand())


handler = Handler(check_func, process_func)
