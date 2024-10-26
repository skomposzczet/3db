import time


class Timer:
    def __init__(self):
        self.elapsed_time = 0
        self.t = 0

    def start(self):
        self.t = time.process_time()

    def stop(self):
        self.elapsed_time += time.process_time() - self.t

    def get_elapsed_time(self):
        return self.elapsed_time
