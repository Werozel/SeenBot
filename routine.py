import globals
from PIL import ImageFile
from vk_api.bot_longpoll import VkBotEventType
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
    ImageFile.LOAD_TRUNCATED_IMAGES = True
    handlers.init_handlers()
    print("Created!")

    # TODO check message overflow
    exiting: bool = False
    while not exiting:
        try:
            while True:
                for event in globals.longpoll.listen():
                    if event.type == VkBotEventType.MESSAGE_NEW:
                        msg = event.obj.message
                        handlers.handle_msg(msg)
        except TimeoutError:
            print(traceback.format_exc())
            pass
        except Exception:
            print(traceback.format_exc())
            break

    globals.session.close_all()
    globals.engine.dispose()
    globals.pool.get().close()
    sys.exit(0)
