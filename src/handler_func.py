import multiprocessing
from libs.Handler import Handler
from src.handlers.is_alive_handler import handler as is_alive_handler
from src.handlers.help_handler import handler as help_handler
from src.handlers.new_phrase_handler import handler as new_phrase_handler
from src.handlers.show_phrases_handler import handler as show_phrases_handler
from src.handlers.remove_phrase_handler import handler as remove_phrase_handler

handlers = []


def add_handler(handler: Handler):
    handlers.append(handler)


def handle_msg(msg):
    for handler in handlers:
        if handler.check(msg):
            handler.process(msg)

def init_handlers():
    add_handler(is_alive_handler)
    add_handler(help_handler)
    add_handler(new_phrase_handler)
    add_handler(show_phrases_handler)
    add_handler(remove_phrase_handler)
