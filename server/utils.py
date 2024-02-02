import time
from typing import Callable
import pygame as pg

def time_it(func):
    def wrapper(*args, **kwargs):
        t1 = time.time()
        result = func(*args, **kwargs)
        t2 = time.time()
        print(f'{func.__name__}: {t2-t1}')
        return result
    return wrapper

class Timer:
    def __init__(self, default_time:int) -> None:
        self.default_ticks = default_time * 1000
        self.time_left = default_time
        self.active = False
        self.start_ticks = None
        self.callback = None

    def start(self, callback: Callable=None):
        print(self)
        self.callback = callback
        self.start_ticks = pg.time.get_ticks()
        self.active = True

    def check(self) -> int:
        if self.active:
            current_ticks = pg.time.get_ticks()
            run_time = current_ticks - self.start_ticks
            self.time_left = (self.default_ticks - run_time)//1000

            if self.time_left <= 0:
                self.complete()

            return self.time_left

    def cancel(self):
        self.time_left = self.default_ticks//1000
        self.active = False
        self.start_ticks = None
        self.callback = None
    
    def complete(self):
        if self.callback:
            self.callback()

        self.time_left = self.default_ticks//1000
        self.active = False
        self.start_ticks = None
        self.callback = None


    





    