from typing import List

from libs.Handler import Handler
from globals import api, get_rand, pool, session_factory, format_time
from src.comparison import rms_compare
from libs.PictureSize import PictureSize
from libs.Picture import Picture
from libs.Phrase import Phrase
from libs.User import User
from libs.PicMessage import PicMessage
import time
import threading
import requests


def get_attachments(fwd) -> list:
    if fwd is None or len(fwd) == 0:
        return []
    res = []
    for msg in fwd:
        res += msg.get('attachments') + get_attachments(msg.get('fwd_messages'))
    return res


def was_seen(url: str, size: str) -> dict:
    session = session_factory()
    # Checking whether a link is already in DB 
    pic_already_in_db = session.query(PictureSize).filter(PictureSize.link == url).first()
    session.close()
    if pic_already_in_db:
        # Already in DB
        print("Same link", flush=True)
        return {'result': True, 'simpic': pic_already_in_db}
    # Not in DB
    raw_pic = requests.get(url).content  # Getting a picture from VK
    # Getting all pictures with same max size
    all_pics_with_same_size: List[PictureSize] = session.query(PictureSize).filter(PictureSize.size == size).all()
    # Starting async_pool to compare all of pictures with same size with current
    results = [pool.get().apply_async(rms_compare, args=(i, raw_pic,)) for i in all_pics_with_same_size]
    for res, pic in [i.get() for i in results]:
        if res < 10:
            # Pictures are similar enough
            print("Already seen, has similar picture", flush=True)
            return {'result': True, 'simpic': pic}
    print("No similar pic, returning...", flush=True)
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
    
    start_time = time.time()
    # Count of seen pictures
    seen_cnt = 0
    for pic in photos:
        sizes = pic.get('sizes')  # All sizes for this picture
        pic_id = pic.get('id')

        # FIXME not sure if an order of sizes is consistent
        max_size: dict = sizes[-1]  # Max size of this picture
        middle_size: dict = sizes[int(len(sizes) / 2)]
        # Checking if a max size of this picture has been already seen
        result_max = was_seen(max_size.get('url'), max_size.get('type'))
        result_middle = was_seen(middle_size.get('url'), middle_size.get('type'))

        if result_max.get('result') or result_middle.get('result'):
            # Already seen
            picture_size: PictureSize = result_max.get('simpic') if result_max.get('result') \
                                                              else result_middle.get('simpic')
            picture: Picture = Picture.get(picture_size.pic_id) if picture_size else None
            user: User = User.get(picture.user_id) if picture else None
            if user:
                seen_message += f'Отправил {user.first_name} ' \
                                f' {user.last_name} в' \
                                f'  {format_time(picture_size.add_time)}\n'
            seen_cnt += 1
        else:
            # New picture
            # Adding it to the DB
            picture_size = Picture(pic_id, sender_id)
            session.add(picture_size)
            session.commit()
            session.add(PictureSize(pic_id, max_size.get('type'), max_size.get('url')))
            session.add(PicMessage(sender_id, pic_id, msg.get('text')))
            session.commit()

    end_time = time.time()
    print(f"Checked in {end_time - start_time}")

    # Adding negative carma for each seen picture
    user.downs += seen_cnt
    session.add(user)
    session.commit()
    # Sending a message if any picture was not new
    if seen_cnt > 0:
        peer_id = msg.get('peer_id')
        api.messages.send(peer_id=peer_id,
                          message=seen_message,
                          random_id=get_rand())
    session.close()


def process_func(msg):
    # Leaving a thread that processes this message running 
    threading.Thread(target=process_pic, args=(msg, ), daemon=True).start()


handler = Handler(check_func, process_func)

