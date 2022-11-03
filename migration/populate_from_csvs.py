from globals import session
import pandas as pd
from datetime import datetime

# Necessary imports
from libs.Achievement import Achievement
from libs.Phrase import Phrase
from libs.DownloadedPic import DownloadedPic
from libs.RawLink import RawLink
from libs.PicMessage import PicMessage
from libs.PictureSize import PictureSize
from libs.Picture import Picture
from libs.User import User


def datetime_from_string(s: str) -> datetime:
    return datetime.strptime(s, "%Y-%m-%d %H:%M:%S")


def read_csv(filename: str) -> pd.DataFrame:
    return pd.read_csv(filename, sep=';', engine='python')


def populate_phrases():
    df: pd.DataFrame = read_csv("phrases.csv")
    for _, row in df.iterrows():
        phrase = Phrase(
            id=int(row['id']),
            text=row['text'],
            add_time=datetime_from_string(row['add_time']),
            user_id=int(row['user_id'])
        )
        session.add(phrase)
    session.commit()


def populate_users():
    df: pd.DataFrame = read_csv("users.csv")
    for _, row in df.iterrows():
        user = User(
            id=int(row['id']),
            first_name=row['first_name'],
            last_name=row['last_name'],
            ups=int(row['ups']),
            downs=int(row['downs']),
            bads=int(row['bads']),
            all_pics=int(row['all_pics']),
            add_time=datetime_from_string(row['add_time'])
        )
        session.add(user)
    session.commit()


def populate_pictures():
    df: pd.DataFrame = read_csv("pictures.csv")
    for _, row in df.iterrows():
        picture = Picture(
            id=int(row["id"]),
            ups=int(row["ups"]),
            downs=int(row["downs"]),
            bads=int(row["bads"]),
            user_id=int(row["user_id"]),
            owner_id=int(row["owner_id"]),
            access_key=row["access_key"],
            add_time=datetime_from_string(row["add_time"])
        )
        session.add(picture)
    session.commit()


def populate_sizes():
    df: pd.DataFrame = read_csv("sizes.csv")
    for _, row in df.iterrows():
        pic_size = PictureSize(
            id=int(row["id"]),
            pic_id=int(row["pic_id"]),
            size=row["size"],
            link=row["link"],
            add_time=datetime_from_string(row["add_time"])
        )
        session.add(pic_size)
    session.commit()


def populate_messages():
    df: pd.DataFrame = read_csv("messages.csv")
    for _, row in df.iterrows():
        msg = PicMessage(
            id=int(row["id"]),
            user_id=int(row["user_id"]),
            pic_id=int(row["pic_id"]),
            time=datetime_from_string(row["time"]),
            text=row["text"]
        )
        session.add(msg)
    session.commit()


def populate_raw_links():
    df: pd.DataFrame = read_csv("raw_links.csv")
    for _, row in df.iterrows():
        raw_link = RawLink(
            id=int(row["id"]),
            type=row["type"],
            owner_id=int(row["owner_id"]),
            access_key=row["access_key"],
            track_code=row["track_row"],
            url=row["url"],
            user_id=int(row["user_id"]),
            add_time=datetime_from_string("add_time")
        )
        session.add(raw_link)
    session.commit()


def populate_downloaded_pics():
    df: pd.DataFrame = read_csv("downloaded_pics.csv")
    for _, row in df.iterrows():
        downloaded_pic = DownloadedPic(
            id=int(row["id"]),
            picture_id=int(row["picture_id"]),
            album_id=row["album_id"],
            owner_id=int(row["owner_id"]),
            access_key=row["access_key"]
        )
        session.add(downloaded_pic)
    session.commit()


def main():
    populate_users()
    populate_pictures()
    populate_sizes()
    populate_messages()
    populate_raw_links()
    populate_downloaded_pics()
    populate_phrases()


if __name__ == "__main__":
    main()
