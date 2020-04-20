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


def get_attachments(fwd):
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
        return {"result": True, "simlink": url}
    all_pics_with_same_size = session.query(PictureSize.link).filter(PictureSize.size == size).all()
    results = [pool.apply_async(rmsCompare, args=(i, url,)) for i in all_pics_with_same_size]
    for res, s in [i.get() for i in results]:
        if res < 10:
            print("Already seen, has similar picture", flush=True)
            session.close()
            return {"result": True, "simlink": s}
    print("No similar pic, returning...", flush=True)
    session.close()
    return {"result": False, "simlink": None}


def check_func(msg):
    att = msg.get('attachments') + get_attachments(msg.get('fwd_messages'))
    return len(att) > 0 and any(list(map(lambda x: x.get('type') == 'photo', att)))


def process_pic(msg):
    attachments = msg.get('attachments') + get_attachments(msg.get('fwd_messages'))
    photos = list(map(lambda x: x.get('photo'), list(filter(lambda x: x.get('type') == 'photo', attachments))))
    sender_id = msg.get('from_id')
    user = User.get(sender_id)
    
    start_time = time.time()
    seen_flag = False
    for pic in photos:
        max_size: dict = None
        for size in reversed(size_letters):
            if max_size is not None:
                break
            for i in att.get("photo").get("sizes"):
                if i.get("type") == size:
                    max_size = i
                    break
        threading.Thread(target=was_seen, args=())


    end_time = time.time()
    print(f"Checked in {end_time - start_time}")

    if seen_flag:
        peer_id = msg.get('peer_id')
        api.messages.send(peer_id = peer_id,
                          message=Phrase.get_random(),
                          random_id=get_rand())

def process_func(msg):
    pass

handler = Handler(check_func, process_func)