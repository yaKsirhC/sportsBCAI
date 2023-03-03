import time
from colorama import Fore

class py_timer:
    def __init__(self):
        start = time.time()
        self.start = start
    def print_time_elapsed(self):
        end = time.time()
        dt = end - self.start
        print('Time Elapsed: '+ Fore.BLUE + str(round(dt, 8)) + 's' + Fore.WHITE)