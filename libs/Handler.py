

class Handler:

    # check_func and process_func take message as an argument
    def __init__(self, check_func, process_func):
        self.check = check_func
        self.process = process_func
