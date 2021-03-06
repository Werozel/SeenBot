from libs.Handler import Handler
from globals import api, get_attachments, get_rand
import random


mashup_phrases = ["Пиздец", "Полный пиздец", "Пиздец нахуй", "Ебанутый"]


def check_func(msg):
    if msg.get('from_id') != 63448544:
        return False
    att = msg.get('attachments') + get_attachments(msg.get('fwd_messages'))
    return len(att) > 0 and any(list(map(lambda x: x.get('type') == 'audio', att)))


def process_func(msg):
    peer_id = msg.get('peer_id')
    api.messages.send(peer_id=peer_id,
                      message=random.choice(mashup_phrases),
                      random_id=get_rand())


handler = Handler(check_func, process_func)
