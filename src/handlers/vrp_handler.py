from globals import api, get_rand, session
from libs.Handler import Handler
from libs.Picture import Picture


def check_func(msg):
    text = msg.get('text')
    return text.startswith("Баян, врп") or text.startswith("Баян, рандом")


def process_func(msg):
    random_pic = Picture.get_random_pic(session)
    # TODO: Attach picture
    peer_id = msg.get('peer_id')
    api.messages.send(peer_id=peer_id,
                      message="Готово",
                      random_id=get_rand())


handler = Handler(check_func, process_func)
