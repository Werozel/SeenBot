from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import vk_api
from vk_api.bot_longpoll import VkBotLongPoll
import config
import datetime
import random

engine = create_engine(f"postgresql://{config.db_username}:{config.db_password}@{config.db_host}:{config.db_port}/{config.db_name}")
SessionFactory = sessionmaker()
SessionFactory.configure(bind=engine, autocommit=True)
session = SessionFactory()
Base = declarative_base()

vk_session = vk_api.VkApi(token=config.vk_secret)
longpoll = VkBotLongPoll(vk_session, config.vk_groupId)

api = vk_session.get_api()


def timestamp():
    return datetime.datetime.now()

def get_rand() -> int:
    return random.randint(1, 9223372036854775807 - 1)
