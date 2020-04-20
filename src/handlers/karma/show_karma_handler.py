from libs.Handler import Handler
from globals import api, get_rand, session
from libs.User import User

def check_func(msg):
    text = msg.get('text')
    return text.startswith("Баян, стат")


def process_func(msg):
    users = session.query(User).all()
    stats: list = list(map(lambda x: x.show_stat(), users))
    stat_str = '\n'.join(stats)
    peer_id = msg.get('peer_id')
    api.messages.send(peer_id = peer_id,
                     message=stat_str,
                     random_id=get_rand())

handler = Handler(check_func, process_func)