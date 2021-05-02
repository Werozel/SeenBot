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
import constants

engine = create_engine(f"postgresql://{config.db_username}:{config.db_password}@"
                       f"{config.db_host}:{config.db_port}/{config.db_name}")
session_factory = sessionmaker(bind=engine)
session = session_factory()
Base = declarative_base()

vk_session = vk_api.VkApi(token=config.vk_secret)
vk_upload = vk_api.upload.VkUpload(vk_session)
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


def get_month_start() -> datetime.datetime:
    return timestamp().replace(day=1, hour=0, minute=0, second=0, microsecond=0)


def format_time(date: datetime.datetime) -> str:
    return date.strftime("%H:%M,  %d %b")


def format_vrp_time(date: datetime.datetime) -> str:
    return date.strftime("%d %b %Y")


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
    from libs.DownloadedPic import DownloadedPic
    Base.metadata.create_all(engine)


def intersection(list1: list, list2: list) -> list:
    res = []
    for x in list1:
        if x in list2:
            res.append(x)
    return res


def sort_sizes(unsorted_sizes: list) -> list:
    res = []
    for x in constants.size_letters:
        if x in unsorted_sizes:
            res.append(x)
    return res