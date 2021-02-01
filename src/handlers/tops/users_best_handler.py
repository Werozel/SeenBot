from globals import api, get_rand, session
from libs.Handler import Handler
from libs.Picture import Picture

import datetime


def check_func(msg):
    text = msg.get('text')
    return text.startswith("Баян, мой топ")


def process_func(msg):
    Picture.get_best_for_user(msg.get('from_id'), session)
    # TODO: Add all pictures
    peer_id = msg.get('peer_id')
    api.messages.send(peer_id=peer_id,
                      message="Готово",
                      random_id=get_rand())


handler = Handler(check_func, process_func)
