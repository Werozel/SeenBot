from typing import List

from globals import api, get_rand, session_factory, format_vrp_time
from libs.Handler import Handler
from libs.Picture import Picture


def check_func(msg):
    text: str = msg.get('text')
    result = text.startswith("Баян, врп") or text.startswith("Баян, рандом")
    tail = text.replace("Баян, врп", "").replace("Баян, рандом", "")
    count = 1
    try:
        count = int(tail)
    except ValueError:
        pass
    return result, count


def process_func(msg, count: int = 1):
    peer_id = msg.get('peer_id')
    if count < 1:
        api.messages.send(peer_id=peer_id,
                          message="Количество фото не может быть меньше одного",
                          random_id=get_rand())
    if count > 10:
        api.messages.send(peer_id=peer_id,
                          message="Количество фото не может быть больше 10",
                          random_id=get_rand())
    local_session = session_factory()
    random_pics: List[Picture] = [Picture.get_random_pic(local_session) for _ in range(0, count)]
    api_string = ",".join([random_pic.get_api_string(peer_id, local_session) for random_pic in random_pics])
    formatted_time = ", ".join([format_vrp_time(random_pic.add_time) for random_pic in random_pics])
    api.messages.send(peer_id=peer_id,
                      message=formatted_time,
                      random_id=get_rand(),
                      attachment=api_string)
    local_session.close()


handler = Handler(check_func, process_func)
