import globals
from libs.User import User
from libs.Picture import Picture
from vk_api.bot_longpoll import VkBotEventType
import src.handler_func as handlers
import traceback

if __name__ == "__main__":
    # globals.Base.metadata.create_all(globals.engine)
    handlers.init_handlers()
    print("Created!")


    try:
        for event in globals.longpoll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW and event.from_chat:
                print("New event!")
                msg = event.obj.message
                print(msg)
                handlers.handle_msg(msg)
            raise Exception("Exit")
    except Exception as e:
        print(traceback.format_exc())
    
    globals.session.close()
    globals.engine.dispose()
    # globals.pool.close()