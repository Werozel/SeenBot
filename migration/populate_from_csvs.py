from globals import session
import pandas as pd
from datetime import datetime

# Necessary imports
from libs.Phrase import Phrase
from libs.Achievement import Achievement
from libs.DownloadedPic import DownloadedPic
from libs.RawLink import RawLink
from libs.PicMessage import PicMessage
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
    pass


def populate_sizes():
    pass


def populate_messages():
    pass


def populate_raw_links():
    pass


def populate_downloaded_pics():
    pass


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
