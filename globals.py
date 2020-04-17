from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from vk_api.bot_longpoll import VkBotLongPoll
import vk_api
import config
import datetime
import random
import multiprocessing, signal
import pytz

engine = create_engine(f"postgresql://{config.db_username}:{config.db_password}@{config.db_host}:{config.db_port}/{config.db_name}")
SessionFactory = sessionmaker()
SessionFactory.configure(bind=engine, autocommit=True)
session = SessionFactory()
Base = declarative_base()

vk_session = vk_api.VkApi(token=config.vk_secret)
longpoll = VkBotLongPoll(vk_session, config.vk_groupId)
api = vk_session.get_api()

size_letters = ('m', 'o', 'p', 'q', 'r', 's', 'x', 'y', 'z')

def worker_init():
    def handler(signum, stack):
        exit(0)
    signal.signal(signal.SIGINT, handler)

# pool = multiprocessing.Pool(processes=32,initializer=worker_init)


def timestamp() -> datetime.datetime:
    tz = pytz.timezone("Europe/Moscow")
    return datetime.datetime.now(tz)

def format_time(date: datetime.datetime) -> str:
    return date.strftime("%H:%M&#12288;%d %b")

def days_between(date1: datetime.datetime, date2: datetime.datetime) -> int:
    d1 = date1.replace(tzinfo=None)
    d2 = date2.replace(tzinfo=None)
    return abs((d1 - d2).days)

def get_rand() -> int:
    return random.randint(1, 9223372036854775807 - 1)
