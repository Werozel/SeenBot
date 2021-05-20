from typing import Tuple, List

from globals import session_factory
from vk_api.audio import VkAudio
import vk_api
import login_config
from libs.RawLink import RawLink


def two_factor() -> Tuple[str, bool]:
    code = input("Code? ")
    return code, True


vk_session = vk_api.VkApi(login_config.LOGIN, login_config.PASSWORD, auth_handler=two_factor)
vk_session.auth()

vk_audio = VkAudio(vk_session)

local_session = session_factory()

all_audio: List[RawLink] = local_session.query(RawLink).filter(RawLink.type == 'audio').all()

for audio in all_audio:
    audio_obj: dict = vk_audio.get_audio_by_id(audio.owner_id, audio.id)
    audio.url = audio_obj.get('url')
    audio.track_code = audio_obj.get('track_code')
    local_session.add(audio)

local_session.commit()
local_session.close()
