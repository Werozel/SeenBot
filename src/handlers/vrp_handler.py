from globals import api, get_rand, session
from libs.Handler import Handler
from libs.Picture import Picture


def check_func(msg):
    text = msg.get('text')
    return text.startswith("Баян, врп") or text.startswith("Баян, рандом")


def process_func(msg):
    random_pic: Picture = Picture.get_random_pic(session)
    peer_id = msg.get('peer_id')
    api.messages.send(peer_id=peer_id,
                      message="Готово",
                      random_id=get_rand(),
                      attachment=random_pic.to_api_string())


handler = Handler(check_func, process_func)
