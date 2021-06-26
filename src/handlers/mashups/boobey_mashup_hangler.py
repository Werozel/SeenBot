from libs.Handler import Handler
from globals import api, get_attachments, get_rand
import random

from src.balabola_api import get_random_text, StylesEnum

mashup_phrases = ["Пиздец", "Полный пиздец", "Пиздец нахуй", "Ебанутый"]
balabola_phrases = [
    "Мэшап послушан",
    "Заскамил мамонта его имя Иван Убеев",
    "Иван Убеев",
    "Пожилой абоба",
    "Неизвестен - Без названия"
]


def check_func(msg):
    if msg.get('from_id') != 63448544:
        return False
    att = msg.get('attachments') + get_attachments(msg.get('fwd_messages'))
    return len(att) > 0 and any(list(map(lambda x: x.get('type') == 'audio', att)))


def process_func(msg):
    peer_id = msg.get('peer_id')
    random_text = get_random_text(
        random.choice(balabola_phrases),
        random.choice(list(StylesEnum))
    )
    if random_text:
        phrase = random_text
    else:
        phrase = random.choice(mashup_phrases)
    api.messages.send(peer_id=peer_id,
                      message=phrase,
                      random_id=get_rand())


handler = Handler(check_func, process_func)
