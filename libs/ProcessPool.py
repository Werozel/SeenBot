import multiprocessing
import sys


class ProcessPool:

    pool = None

    def get(self):
        return self.pool