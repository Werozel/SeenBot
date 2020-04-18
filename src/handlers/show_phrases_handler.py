from libs.Handler import Handler
from globals import api, get_rand
from libs.Phrase import Phrase

def check_func(msg):
    text = msg.get('text')
    return text.startswith("Баян, фразы")


def process_func(msg):
    peer_id = msg.get('peer_id')
    message = Phrase.get_all()
    print("message: " + message)
    api.messages.send(peer_id = peer_id,
                      message= message if message != "" and message else "Нет ни одной фразы!",
                      random_id=get_rand())

handler = Handler(check_func, process_func)