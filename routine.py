import globals
from libs.User import User
from libs.Picture import Picture
from vk_api.bot_longpoll import VkBotEventType
from libs.ProcessPool import ProcessPool
import src.handler_func as handlers
import traceback
import multiprocessing
import sys

if __name__ == "__main__":
    if sys.platform.startswith('linux'):
        print('Running on linux')
        globals.pool.pool = multiprocessing.Pool(processes=32, initializer=globals.worker_init)
    elif sys.platform.startswith('win32'):
        print('Running on windows')
        globals.pool.pool = multiprocessing.Pool(processes=32)
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
    globals.pool.get().close()
