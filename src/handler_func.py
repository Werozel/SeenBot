import multiprocessing
from libs.Handler import Handler
import src.handlers.is_alive_handler as is_alive_handler

handlers = []


def add_handler(handler: Handler):
    handlers.append(handler)


def handle_msg(msg):
    for handler in handlers:
        if handler.check(msg):
            handler.process(msg)

def init_handlers():
    add_handler(is_alive_handler.handler)

