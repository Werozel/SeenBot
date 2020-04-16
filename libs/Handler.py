

class Handler:

    def __init__(self, command, process_func):
        self.command = command
        self.process = process_func

    def invoke(self, **kwargs):
        return self.process(**kwargs)