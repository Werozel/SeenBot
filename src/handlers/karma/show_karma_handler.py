from libs.Handler import Handler
from globals import api, get_rand, session
from sqlalchemy import desc
from libs.User import User

def check_func(msg):
    text = msg.get('text')
    return text.startswith("Баян, стат")


def process_func(msg):
    users = session.query(User).order_by().all()
    stats: list = list(map(lambda x: x.show_stat(), 
                       sorted(users, key=lambda user: (user.downs / user.all_pics if user.all_pics > 0 else -1000, 
                                                       -user.ups/user.all_pics if user.all_pics > 0 else -1000, ))))
    stat_str = '\n'.join(stats)
    peer_id = msg.get('peer_id')
    api.messages.send(peer_id = peer_id,
                     message=stat_str,
                     random_id=get_rand())

handler = Handler(check_func, process_func)