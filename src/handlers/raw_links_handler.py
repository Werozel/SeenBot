from globals import get_attachments, get_rand, api, format_time, session
from libs.Phrase import Phrase
from libs.RawLink import RawLink
from libs.Handler import Handler
from libs.User import User


def check_func(msg):
    return any(
        map(
            lambda x: x.get('type') in ['audio', 'video'],
            msg.get('attachments') + get_attachments(msg.get('fwd_messages'))
        )
    )


def process_func(msg):
    peer_id = msg.get('peer_id')
    atts = list(
        filter(
            lambda x: x.get('type') in ['audio', 'video'],
            msg.get('attachments') + get_attachments(msg.get('fwd_messages'))
        )
    )
    for att in atts:
        type = att.get('type')
        obj = att.get(type)
        id = obj.get('id')
        existing_obj: RawLink = RawLink.get(id)
        if existing_obj:
            orig_user: User = User.get(existing_obj.user_id)
            orig_user.downs += 1
            session.add(orig_user)
            seen_message = Phrase.get_random().split(':')[1].strip() + '\n'
            seen_message += f'Отправил  {orig_user.first_name}' \
                            f' {orig_user.last_name}  в' \
                            f'  {format_time(existing_obj.add_time)}\n'
            api.messages.send(peer_id=peer_id,
                              message=seen_message,
                              random_id=get_rand())
            session.add(orig_user)
        else:
            new_raw_link_obj = RawLink(
                id=obj.get('id'),
                type=type,
                owner_id=obj.get('owner_id'),
                access_key=obj.get('access_key'),
                user_id=msg.get('from_id')
            )
            session.add(new_raw_link_obj)
    session.commit()


handler = Handler(check_func, process_func)
