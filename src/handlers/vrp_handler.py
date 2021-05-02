from typing import Optional

from globals import api, get_rand, session_factory, vk_upload
from libs.DownloadedPic import DownloadedPic
from libs.Handler import Handler
from libs.Picture import Picture
import wget
import os


def check_func(msg):
    text = msg.get('text')
    return text.startswith("Баян, врп") or text.startswith("Баян, рандом")


def process_func(msg):
    peer_id = msg.get('peer_id')
    local_session = session_factory()
    random_pic: Picture = Picture.get_random_pic(local_session)
    downloaded_pic: Optional[DownloadedPic] = DownloadedPic.get(random_pic.id, local_session)
    if downloaded_pic is None:
        file_name = wget.download(random_pic.get_best_size(local_session).link)
        photo_obj: dict = vk_upload.photo_messages(file_name, peer_id=peer_id)[0]
        os.remove(file_name)
        downloaded_pic = DownloadedPic(
            id=photo_obj.get('id'),
            album_id=photo_obj.get('album_id'),
            owner_id=photo_obj.get('owner_id'),
            access_key=photo_obj.get('access_key')
        )
        local_session.add(downloaded_pic)
        local_session.commit()

    api_string = downloaded_pic.get_api_str()
    api.messages.send(peer_id=peer_id,
                      random_id=get_rand(),
                      attachment=api_string)


handler = Handler(check_func, process_func)
