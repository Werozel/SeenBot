from globals import api, get_rand, session_factory, format_vrp_time
from libs.Handler import Handler
from libs.Picture import Picture


def check_func(msg):
    text = msg.get('text')
    return text.startswith("Баян, врп") or text.startswith("Баян, рандом")


def process_func(msg):
    peer_id = msg.get('peer_id')
    local_session = session_factory()
    random_pic: Picture = Picture.get_random_pic(local_session)
    api_string = random_pic.get_api_string(peer_id, local_session)
    api.messages.send(peer_id=peer_id,
                      message={format_vrp_time(random_pic.add_time)},
                      random_id=get_rand(),
                      attachment=api_string)


handler = Handler(check_func, process_func)
