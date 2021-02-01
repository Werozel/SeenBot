from libs.Handler import Handler
from src.handlers.is_alive_handler import handler as is_alive_handler
from src.handlers.help_handler import handler as help_handler
from src.handlers.phrase.new_phrase_handler import handler as new_phrase_handler
from src.handlers.phrase.show_phrases_handler import handler as show_phrases_handler
from src.handlers.phrase.remove_phrase_handler import handler as remove_phrase_handler
from src.handlers.exit_handler import handler as exit_handler
from src.handlers.picture_handler import handler as picture_handler
from src.handlers.karma.show_karma_handler import handler as show_karma_handler
from src.handlers.karma.add_positive_karma import handler as add_positive_karma
from src.handlers.karma.add_negative_karma import handler as add_negative_karma
from src.handlers.mashup_hangler import handler as mashup_handler
from src.handlers.raw_links_handler import handler as raw_links_handler
from src.handlers.karma.add_bads_karma import handler as bads_handler
from src.handlers.vrp_handler import handler as vrp_handler
from src.handlers.tops.montly_top_handler import handler as monthly_top_handler
from src.handlers.tops.users_best_handler import handler as users_best_handler

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
    add_handler(exit_handler)
    add_handler(picture_handler)
    add_handler(show_karma_handler)
    add_handler(add_positive_karma)
    add_handler(add_negative_karma)
    add_handler(mashup_handler)
    add_handler(raw_links_handler)
    add_handler(bads_handler)
    add_handler(vrp_handler)
    add_handler(monthly_top_handler)
    add_handler(users_best_handler)
