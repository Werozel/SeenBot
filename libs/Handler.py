

class Handler:

    # check_func and process_func take message as an argument
    def __init__(self, check_func, process_func):
        self.check = check_func
        self.process = process_func

    def handle_message(self, msg):
        check_result = self.check(msg)
        if isinstance(check_result, bool) and check_result:
            self.process(msg)
        elif isinstance(check_result, tuple) and check_result[0]:
            self.process(msg, *check_result[1:])  # Removing first true/false
