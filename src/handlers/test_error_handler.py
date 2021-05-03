from libs.Handler import Handler


def check_func(msg):
    text = msg.get('text')
    return text.startswith("Баян, ошибка")


def process_func(_):
    raise Exception("Test exception")


handler = Handler(check_func, process_func)

