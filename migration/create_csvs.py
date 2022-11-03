from typing import List
from libs.DownloadedPic import DownloadedPic
from libs.Phrase import Phrase
from libs.PicMessage import PicMessage

import csv

from libs.Picture import Picture
from libs.PictureSize import PictureSize
from libs.RawLink import RawLink
from libs.User import User


def write_csv(filename: str, rows: List[str]):
    with open(filename, "w", newline='') as file:
        writer = csv.writer(file, delimiter=";")
        writer.writerows(rows)


def put_phrases():
    phrases: List[Phrase] = Phrase.get_all()

    rows = [["id", "text", "add_time", "user_id"], *list(
        map(
            lambda x: [x.id, x.text, x.add_time, x.user_id],
            phrases
        )
    )]

    write_csv("phrases.csv", rows)


def put_downloaded_pics():
    downloaded_pics = DownloadedPic.get_all()

    rows = [["id", "picture_id", "album_id", "owner_id", "access_key"], *list(
        map(
            lambda x: [x.id, x.picture_id, x.album_id, x.owner_id, x.access_key],
            downloaded_pics
        )
    )]

    write_csv("downloaded_pics.csv", rows)


def put_messages():
    messages = PicMessage.get_all()

    rows = [['id', 'user_id', 'pic_id', 'time', 'text'], *list(
        map(
            lambda x: [x.id, x.user_id, x.pic_id, x.time, x.text],
            messages
        )
    )]

    write_csv("messages.csv", rows)


def put_pictures():
    pictures = Picture.get_all()

    rows = [['id', 'ups', 'downs', 'bads', 'user_id', 'owner_id', 'access_key', 'add_time'], *list(
        map(
            lambda x: [x.id, x.ups, x.downs, x.bads, x.user_id, x.owner_id, x.access_key, x.add_time],
            pictures
        )
    )]

    write_csv("pictures.csv", rows)


def put_raw_links():
    raw_links = RawLink.get_all()

    rows = [['id', 'type', 'owner_id', 'access_key', 'track_code', 'url', 'user_id', 'add_time'], *list(
        map(
            lambda x: [x.id, x.type, x.owner_id, x.access_key, x.track_code, x.url, x.user_id, x.add_time],
            raw_links
        )
    )]

    write_csv("raw_links.csv", rows)


def put_sizes():
    sizes = PictureSize.get_all()

    rows = [['id', 'pic_id', 'size', 'link', 'add_time'], *list(
        map(
            lambda x: [x.id, x.pic_id, x.size, x.link, x.add_time],
            sizes
        )
    )]

    write_csv("sizes.csv", rows)


def put_users():
    users = User.get_all()

    rows = [['id', 'first_name', 'last_name', 'ups', 'downs', 'bads', 'all_pics', 'add_time'], *list(
        map(
            lambda x: [x.id, x.first_name, x.last_name, x.ups, x.downs, x.bads, x.all_pics, x.add_time],
            users
        )
    )]

    write_csv("users.csv", rows)


def main():
    put_phrases()
    put_downloaded_pics()
    put_messages()
    put_pictures()
    put_raw_links()
    put_sizes()
    put_users()


if __name__ == "__main__":
    main()
