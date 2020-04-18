from libs.Handler import Handler
from globals import api, get_rand

def check_func(msg):
    text = msg.get('text')
    return text.startswith("Баян, off") and msg.get('from_id') == 127463953


def process_func(msg):
    peer_id = msg.get('peer_id')
    api.messages.send(peer_id = peer_id,
                     message="Готово",
                     random_id=get_rand())
    raise Exception("Exiting...")
    

handler = Handler(check_func, process_func)