from libs.Handler import Handler
from globals import api, get_rand

def check_func(msg):
    text = msg.get('text')
    return text.startswith("Баян, жив")


def process_func(msg):
    peer_id = msg.get('peer_id')
    api.messages.send(peer_id = peer_id,
                     message="Живой",
                     random_id=get_rand())

handler = Handler(check_func, process_func)