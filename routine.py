import globals
from libs.User import User
from libs.Picture import Picture

if __name__ == "__main__":
    globals.Base.metadata.create_all(globals.engine)
    globals.session.close()
    print("Done!")