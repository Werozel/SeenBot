from libs.Handler import Handler
from globals import contains_any
from src.handlers.karma.process_alter_karma import Karma, process_func as alter_karma


label: str = "negative_karma"
negative_anchors = ['баян', 'был', 'пикабу', 'говн']


def check_func(msg):
    text = msg.get('text')
    reply_msg = msg.get('reply_message')
    return reply_msg and len(reply_msg.get('attachments')) > 0 and contains_any(text, negative_anchors)


def process_func(msg):
    alter_karma(msg, Karma.NEGATIVE, label)


handler = Handler(check_func, process_func)
