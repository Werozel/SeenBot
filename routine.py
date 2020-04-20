import globals
from libs.User import User
from libs.Picture import Picture
from vk_api.bot_longpoll import VkBotEventType
import src.handler_func as handlers
import traceback
import multiprocessing

if __name__ == "__main__":
    globals.init_pool()
    multiprocessing.freeze_support()
    globals.Base.metadata.create_all(globals.engine)
    handlers.init_handlers()
    print("Created!")

    # TODO check message overflow
    try:
        while True:
            for event in globals.longpoll.listen():
                if event.type == VkBotEventType.MESSAGE_NEW and event.from_chat:
                    msg = event.obj.message
                    handlers.handle_msg(msg)
    except Exception as e:
        print(traceback.format_exc())
    
    globals.session.close()
    globals.engine.dispose()
    # globals.pool.close()