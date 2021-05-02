from typing import Optional

from globals import api, get_rand, session_factory
from libs.User import User
from libs.Handler import Handler
from libs.Picture import Picture


def check_func(msg):
    text = msg.get('text')
    return text.startswith("Баян, мой топ")


def process_func(msg):
    peer_id = msg.get('peer_id')
    local_session = session_factory()
    user_id: int = msg.get('from_id')
    user: Optional[User] = User.get(user_id, local_session)
    best_pictures = Picture.get_best_for_user(user_id, local_session, limit=10)
    attachment_strings = list(
        map(
            lambda x: x.get_api_string(peer_id),
            best_pictures
        )
    )
    local_session.close()
    api.messages.send(peer_id=peer_id,
                      message=f"{user.get_formatted_name()}: топ",
                      attachment=','.join(attachment_strings),
                      random_id=get_rand())


handler = Handler(check_func, process_func)
