import multiprocessing
from libs.Handler import Handler

handlers = []


def add_handler(handler: Handler):
    handlers.append(handler)


def handle_msg(msg):
    for handler in handlers:
        if handler.check(msg):
            handler.process(msg)

