from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from vk_api.bot_longpoll import VkBotLongPoll
from libs.ProcessPool import ProcessPool
import vk_api
import config
import datetime
import random
import signal
import pytz
import re

engine = create_engine(f"postgresql://{config.db_username}:{config.db_password}@"
                       f"{config.db_host}:{config.db_port}/{config.db_name}")
session_factory = sessionmaker()
session_factory.configure(bind=engine)
session = session_factory()
Base = declarative_base()

vk_session = vk_api.VkApi(token=config.vk_secret)
longpoll = VkBotLongPoll(vk_session, config.vk_groupId)
api = vk_session.get_api()


def worker_init():
    def handler(signum, stack):
        exit(0)
    signal.signal(signal.SIGINT, handler)


pool = ProcessPool()


def timestamp() -> datetime.datetime:
    tz = pytz.timezone("Europe/Moscow")
    return datetime.datetime.now(tz)


def format_time(date: datetime.datetime) -> str:
    return date.strftime("%H:%M,  %d %b")


def days_between(date1: datetime.datetime, date2: datetime.datetime) -> int:
    d1 = date1.replace(tzinfo=None)
    d2 = date2.replace(tzinfo=None)
    return abs((d1 - d2).days)


def get_rand() -> int:
    return random.randint(1, 9223372036854775807 - 1)


def get_attachments(fwd) -> list:
    if fwd is None or len(fwd) == 0:
        return []
    res = []
    for msg in fwd:
        res += msg.get('attachments') + get_attachments(msg.get('fwd_messages'))
    return res


# Checks if string s contains any of anchors
def contains_any(s, anchors):
    return any(list(map(lambda x: re.search(x, s, re.IGNORECASE), anchors)))


def log(label, message):
    print(f"{timestamp()}: {label}: {message}", flush=True)


def create_tables():
    from libs.Phrase import Phrase
    from libs.PicMessage import PicMessage
    from libs.PictureSize import PictureSize
    from libs.Picture import PictureSize
    from libs.RawLink import RawLink
    from libs.User import User
    Base.metadata.create_all(engine)
