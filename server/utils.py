import time
from typing import Callable
import pygame as pg
import asyncio

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
        self.default_ticks = default_time
        self.time_left = default_time
        self.active = False
        self.callback = None
        self.task = None

    def start(self, callback: Callable=None):
        self.callback = callback
        self.start_ticks = pg.time.get_ticks()
        self.active = True
        self.task = asyncio.create_task(self._run_timer())

    async def _run_timer(self):
        while self.active and self.time_left > 0:
            await asyncio.sleep(1)
            self.time_left -= 1

        if self.active:  
            self.complete()

    def cancel(self):
        self.time_left = self.default_ticks
        self.active = False
        self.callback = None
    
    def complete(self):
        self.active = False
        if self.callback:
            self.callback()
        self.cancel()


    





    