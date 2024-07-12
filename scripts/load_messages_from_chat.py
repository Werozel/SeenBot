from libs.Picture import Picture
from libs.RawLink import RawLink
from libs.DownloadedPic import DownloadedPic
from libs.User import User
from libs.PictureSize import PictureSize
from libs.PicMessage import PicMessage
import globals
import vk
import config
import constants
import pprint
import time
from src.handler_func import handle_only_karma
import datetime


def handle_message(msg: dict) -> None:
    session = globals.session_factory()
    all_pictures = map(
        lambda x: x.get("photo"),
        filter(
            lambda x: x.get("type") == "photo",
            msg.get("attachments")
        )
    )
    for pic in all_pictures:
        pic_id = pic.get("id")
        pic_date = msg.get("date")
        existing_pic = session.query(Picture).filter(Picture.id == pic_id).first()
        if existing_pic:
            continue
        sender_id = msg.get("from_id")
        if sender_id == constants.COMMUNITY_ID:
            continue
        user: User = session.query(User).filter(User.id == sender_id).first()
        if not user:
            user = User(sender_id)
            session.add(user)
            session.commit()
        picture = Picture(
            id=pic_id,
            user_id=sender_id,
            owner_id=pic.get('owner_id'),
            access_key=pic.get('access_key'),
            time=datetime.datetime.fromtimestamp(pic_date)
        )
        session.add(picture)
        session.commit()

        sizes = pic.get("sizes")
        for size in sizes:
            session.add(
                PictureSize(
                    picture_id=pic_id,
                    size=size.get('type'),
                    link=size.get('url'),
                    time=datetime.datetime.fromtimestamp(pic_date)
                )
            )
        session.add(
            PicMessage(
                user_id=sender_id,
                picture_id=pic_id,
                text=msg.get('text'),
                time=datetime.datetime.fromtimestamp(pic_date)
            )
        )
        session.commit()
    session.close()


if __name__ == "__main__":
    api: vk.API = vk.API(
        access_token=config.vk_user_secret
    )

    last_loaded_date = 1639652562
    # last_loaded_date = 1718178900

    curr_offset = 0
    load_chunk_count = 100

    exiting = False
    while not exiting:
        messages: dict = api.messages.getHistory(
            offset=curr_offset,
            count=load_chunk_count,
            peer_id=config.chat_peer_id,
            v=constants.api_version,
            rev=0,
            externded=1,
        )
        msg_date = None
        for msg in messages.get("items"):
            msg_date = msg.get("date")
            if msg_date <= last_loaded_date:
                exiting = True
                break

            handle_message(msg)
            # handle_only_karma(msg)
        curr_offset += load_chunk_count
        print(f"Loaded {curr_offset} messages, last date = {globals.format_timestamp(msg_date)}")
        time.sleep(2.5)

    pprint.pprint(curr_offset)
