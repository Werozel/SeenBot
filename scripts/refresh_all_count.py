from libs.RawLink import RawLink
from libs.User import User
from libs.Picture import Picture
import globals


if __name__ == "__main__":
    session = globals.session_factory()
    all_users = User.get_all(local_session=session)

    for user in all_users:
        all_user_picks_count = session.query(Picture)\
            .filter(Picture.user_id == user.id)\
            .count()
        user.all_pics = all_user_picks_count
        session.add(user)
        print(user)

    session.commit()
    session.close()
