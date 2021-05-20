from globals import session_factory, format_vrp_time, api, get_rand
from libs.Handler import Handler
from libs.RawLink import RawLink


def check_func(msg):
    text: str = msg.get('text')
    return text.startswith("Баян, мэшап") or text.startswith("Баян, мешап")


def process_func(msg):
    peer_id = msg.get('peer_id')
    local_session = session_factory()
    random_audio: RawLink = RawLink.get_random_audio(local_session)
    formatted_time = format_vrp_time(random_audio.add_time)
    audio_api_str: str = random_audio.get_api_string(peer_id=peer_id)
    api.messages.send(
        peer_id=peer_id,
        message=formatted_time,
        random_id=get_rand(),
        attachments=audio_api_str
    )
    local_session.close()


handler = Handler(check_func, process_func)
