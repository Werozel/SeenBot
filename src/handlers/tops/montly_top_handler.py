from globals import api, get_rand, session
from libs.Handler import Handler
from libs.Picture import Picture

import datetime


def check_func(msg):
    text = msg.get('text')
    return text.startswith("Баян, врп") or text.startswith("Баян, рандом")


def process_func(msg):
    month_timedelta = datetime.timedelta()  # TODO: make month timedelta
    month_ago_dt = datetime.datetime.now() - month_timedelta
    Picture.get_all_from(month_ago_dt, session)
    # TODO: Add all pictures
    peer_id = msg.get('peer_id')
    api.messages.send(peer_id=peer_id,
                      message="Готово",
                      random_id=get_rand())


handler = Handler(check_func, process_func)
