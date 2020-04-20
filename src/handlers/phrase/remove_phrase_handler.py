from libs.Handler import Handler
from globals import api, get_rand, session
from libs.Phrase import Phrase


def check_func(msg):
    text = msg.get('text')
    return text.startswith("Баян, убери фразу") or text.startswith("Баян, удали фразу")


def process_func(msg):
    text = msg.get('text')
    phrase_id = int(text.replace("Баян, убери фразу", "").replace("Баян, удали фразу", "").replace('\n', ''))
    session.delete(Phrase.get(phrase_id))
    session.commit()
    peer_id = msg.get('peer_id')
    api.messages.send(peer_id = peer_id,
                     message="Удалил",
                     random_id=get_rand())

handler = Handler(check_func, process_func)