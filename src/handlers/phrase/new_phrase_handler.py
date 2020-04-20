from libs.Handler import Handler
from globals import api, get_rand, session
from libs.Phrase import Phrase
from libs.User import User


def check_func(msg):
    text = msg.get('text')
    return text.startswith('Баян, добавь фразу') or text.startswith('Баян, новая фраза')


def process_func(msg):
    text = msg.get('text')
    user_id = int(msg.get('from_id'))
    phrase_text = text.replace("Баян, добавь фразу", "").replace("Баян, новая фраза", "").strip().capitalize()
    if not User.get(user_id):
        session.add(User(user_id))
        session.commit()
    session.add(Phrase(text=phrase_text, user_id=user_id))
    session.commit()
    peer_id = msg.get('peer_id')
    api.messages.send(peer_id=peer_id,
                      message="Добавил",
                      random_id=get_rand())

handler = Handler(check_func, process_func)