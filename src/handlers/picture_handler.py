from libs.Handler import Handler
from globals import api, get_rand, pool, session_factory
from constants import size_letters
from src.comparison import rmsCompare
from libs.PictureSize import PictureSize
from libs.Picture import Picture
from libs.Phrase import Phrase
from libs.User import User
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
    pic_size = session.query(PictureSize).filter(PictureSize.link == url).first()
    if pic_size:
        print("Same link", flush=True)
        session.close()
        return {'result': True, 'simlink': url}
    raw_pic = requests.get(url).content
    all_pics_with_same_size = list(map(lambda x: x.link, session.query(PictureSize).filter(PictureSize.size == size).all()))
    results = [pool.get().apply_async(rmsCompare, args=(i, raw_pic,)) for i in all_pics_with_same_size]
    for res, s in [i.get() for i in results]:
        if res < 10:
            print("Already seen, has similar picture", flush=True)
            session.close()
            return {'result': True, 'simlink': s}
    print("No similar pic, returning...", flush=True)
    session.close()
    return {'result': False, 'simlink': None}


def check_func(msg):
    att = msg.get('attachments') + get_attachments(msg.get('fwd_messages'))
    return len(att) > 0 and any(list(map(lambda x: x.get('type') == 'photo', att)))


def process_pic(msg):
    attachments = msg.get('attachments') + get_attachments(msg.get('fwd_messages'))
    photos = list(map(lambda x: x.get('photo'), list(filter(lambda x: x.get('type') == 'photo', attachments))))
    session = session_factory()
    sender_id = msg.get('from_id')
    user: User = session.query(User).filter(User.id==sender_id).first()
    if not User:
        user = User(sender_id)
        session.add(user)
        session.commit()
    user.all_pics += len(attachments)
    
    start_time = time.time()
    seen_cnt = 0
    for pic in photos:
        sizes = pic.get('sizes')
        
        max_size: dict = sizes[-1]
        result = was_seen(max_size.get('url'), max_size.get('type'))
        if result.get('result'):
            seen_cnt += 1
        else:
            pic_id = pic.get('id')
            picture_class = Picture(pic_id, sender_id)
            session.add(picture_class)
            session.commit()
            session.add(PictureSize(pic_id, max_size.get('type'), max_size.get('url')))
            session.commit()

    end_time = time.time()
    print(f"Checked in {end_time - start_time}")

    user.downs += seen_cnt
    session.close()

    if seen_cnt > 0:
        peer_id = msg.get('peer_id')
        api.messages.send(peer_id = peer_id,
                          message=Phrase.get_random().split(':')[1].strip(),
                          random_id=get_rand())

def process_func(msg):
    threading.Thread(target=process_pic, args=(msg, ), daemon=True).start()

handler = Handler(check_func, process_func)