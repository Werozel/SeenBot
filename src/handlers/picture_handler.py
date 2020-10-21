from libs.Handler import Handler
from globals import api, get_rand, pool, session_factory, format_time, log, get_attachments, intersection, session
from src.comparison import rms_compare
from libs.PictureSize import PictureSize
from libs.Picture import Picture
from libs.Phrase import Phrase
from libs.User import User
from libs.PicMessage import PicMessage

import time
import threading


label: str = "picture_handler"


def get_optimal_pair(sizes_with_links: list, sizes: list, pic_id: int):
    pic_sizes = PictureSize.get_sizes_for_id(pic_id, session)
    common_sizes = intersection(sizes, pic_sizes)
    if not common_sizes:
        log(label, f"No common sizes")
        return None, None
    max_common_size = common_sizes[-1]
    optimal_pic: PictureSize = session.query(PictureSize) \
        .filter(PictureSize.pic_id == pic_id, PictureSize.size == max_common_size) \
        .first()
    return optimal_pic, next(x.get('url') for x in sizes_with_links)


def was_seen(sizes_with_links: list) -> dict:
    local_session = session_factory()

    # Checking whether a link is already in DB
    pic_already_in_db = list(map(lambda x: PictureSize.get_by_link(x.get('url'), local_session), sizes_with_links))
    if any(pic_already_in_db):
        # Already in DB
        log(label, "Same link")
        return {'result': True, 'simpic': list(filter(lambda x: x, pic_already_in_db))[0]}

    sizes = list(map(lambda x: x.get('type'), sizes_with_links))
    optimal_sizes_futures = [pool.get().apply_async(get_optimal_pair, args=(sizes_with_links, sizes, pic_id,)) for pic_id in Picture.get_all_ids(local_session)]
    optimal_sizes = []
    for pair in [i.get() for i in optimal_sizes_futures]:
        if pair[0] and pair[1]:
            optimal_sizes.append(pair)

    local_session.close()

    # Starting async_pool to compare all of pictures with same size with current
    results = [pool.get().apply_async(rms_compare, args=(pic, target_url,)) for pic, target_url in optimal_sizes]
    for res, pic in [i.get() for i in results]:
        if res < 10:
            # Pictures are similar enough
            log(label, f"Already seen, has similar picture, id={pic.id}")
            return {'result': True, 'simpic': pic}
    log(label, "No similar pic, returning...")
    return {'result': False, 'simpic': None}


def check_func(msg) -> bool:
    att = msg.get('attachments') + get_attachments(msg.get('fwd_messages'))
    # True if there is any attachments with type 'photo'
    return len(att) > 0 and any(list(map(lambda x: x.get('type') == 'photo', att)))


def process_pic(msg) -> None:
    # Getting all the attachments even in forwarded messages
    attachments = msg.get('attachments') + get_attachments(msg.get('fwd_messages'))
    # Leaving only the photos
    photos = list(map(lambda x: x.get('photo'), list(filter(lambda x: x.get('type') == 'photo', attachments))))
    # New thread - new session
    session = session_factory()
    sender_id = msg.get('from_id')
    # Getting the user from DB or creating a new one
    user: User = session.query(User).filter(User.id == sender_id).first()
    if not User:
        user = User(sender_id)
        session.add(user)
        session.commit()
    user.all_pics += len(photos)
    # Message that will be sent to chat if picture has been already seen
    seen_message = Phrase.get_random().split(':')[1].strip() + '\n'

    seen: bool = False
    start_time = time.time()
    # Count of seen pictures
    for pic in photos:
        sizes = pic.get('sizes')  # All sizes for this picture
        pic_id = pic.get('id')

        # Checking if a max size of this picture has been already seen
        result = was_seen(sizes)

        if result.get('result'):
            # Already seen
            seen = True
            picture_size: PictureSize = result.get('simpic')
            local_session = session_factory()
            picture: Picture = Picture.get(picture_size.pic_id) if picture_size else None
            orig_user: User = User.get(picture.user_id, local_session) if picture else None
            if orig_user:
                seen_message += f'Отправил  {orig_user.first_name}' \
                                f' {orig_user.last_name}  в' \
                                f'  {format_time(picture_size.add_time)}\n'
            local_session.close()
            break
        else:
            # New picture
            # Adding it to the DB
            picture = Picture(pic_id, sender_id)
            session.add(picture)
            session.commit()
            for size in sizes:
                session.add(PictureSize(pic_id, size.get('type'), size.get('url')))
            session.add(PicMessage(sender_id, pic_id, msg.get('text')))
            session.commit()

    end_time = time.time()
    log(label, f"Checked in {end_time - start_time}")

    # Adding negative carma for each seen picture

    # Sending a message if any picture was not new
    if seen:
        log(label, f"{user.first_name} {user.last_name} downs +1 = {user.downs}")
        user.downs += 1
        peer_id = msg.get('peer_id')
        api.messages.send(peer_id=peer_id,
                          message=seen_message,
                          random_id=get_rand())

    session.add(user)
    session.commit()
    session.close()


def process_func(msg):
    # Leaving a thread that processes this message running 
    threading.Thread(target=process_pic, args=(msg, ), daemon=True).start()


handler = Handler(check_func, process_func)
