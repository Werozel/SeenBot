import globals
from libs.User import User
from libs.Picture import Picture
from src.handlers import handle_msg

if __name__ == "__main__":
    globals.Base.metadata.create_all(globals.engine)
    print("Created!")

    while True:
        try:
            for event in globals.longpoll.listen():
                handle_msg(event.msg)
        except Exception as e:
            print("Error!")
    
    globals.engine.close()