from libs.Handler import Handler
from globals import api, get_rand, contains_any, session
from libs.User import User
from libs.Picture import Picture


def check_func(msg):
    text = msg.get('text')
    reply_msg = msg.get('reply_message')
    return reply_msg and len(reply_msg.get('attachments')) > 0 and contains_any(text, ["годн", "заебись", "жиз", "найс", "ор ", "ору "])


def process_func(msg):
    reply_msg = msg.get('reply_message')
    reply_msg_from_id = reply_msg.get('from_id')
    user = User.get(reply_msg_from_id)
    if not user:
        user = User(reply_msg_from_id)
    user.ups += 1
    for att in list(filter(lambda x: x.get('type') == 'photo', reply_msg.get('attachments'))):
        picture = Picture.get(att.get('photo').get('id'))
        picture.ups += 1
        session.add(picture)
    session.add(user)
    session.commit()


handler = Handler(check_func, process_func)