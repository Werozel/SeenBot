from enum import Enum
from libs.User import User
from libs.Picture import Picture
from globals import session, log


class Karma(Enum):
    POSITIVE = 1
    NEGATIVE = 0


def process_func(msg, karma: Karma, label: str):
    reply_msg = msg.get('reply_message')
    reply_msg_from_id = reply_msg.get('from_id')
    user = User.get(reply_msg_from_id)
    if not user:
        user = User(reply_msg_from_id)

    if karma == Karma.POSITIVE:
        user.ups += 1
        log(label, f"{user.first_name} {user.last_name} ups +1 = {user.ups}")
    else:
        user.downs += 1
        log(label, f"{user.first_name} {user.last_name} downs +1 = {user.downs}")
    session.add(user)

    for att in list(filter(lambda x: x.get('type') == 'photo', reply_msg.get('attachments'))):
        picture = Picture.get(att.get('photo').get('id'))
        if picture:
            if karma == Karma.POSITIVE:
                picture.ups += 1
            else:
                picture.downs += 1
            session.add(picture)
    session.commit()
