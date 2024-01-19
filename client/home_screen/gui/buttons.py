from ui_objects.template import TextButton
from typing import Callable
import pygame as pg
from settings import SCREEN_WIDTH, SCREEN_HEIGHT


class StartButton(TextButton):
    def __init__(self, on_click: Callable):
        size = (300, 75)
        x, y = (SCREEN_WIDTH - size[0])//2, SCREEN_HEIGHT//2 + 300,
        super().__init__(
            
            rect=pg.Rect(x, y, size[0], size[1]), 
            text='Start a Game', 
            text_color=(255,255,255), 
            color=(150,150,150), 
            text_size=36
        )
        self.on_click=on_click

    def draw(self, screen: pg.Surface):
        return super().draw(screen)
    
    async def on_click(self):
        await self.on_click()
    

class ExitButton(TextButton):
    def __init__(self, on_click):
        size = (300, 75)
        x, y = (SCREEN_WIDTH - size[0])//2, SCREEN_HEIGHT//2 + 385,
        super().__init__(
            
            rect=pg.Rect(x, y, 300, 75), 
            text='Exit', 
            text_color=(255,255,255), 
            color=(150,150,150), 
            text_size=36
        )
        self.on_click = on_click
    
    def on_click(self):
        self.on_click()

class EnterButton(TextButton):
    def __init__(self, on_click):
        size = (300, 50)
        x, y = (SCREEN_WIDTH - size[0])//2, SCREEN_HEIGHT//2 + 65,
        super().__init__(
            
            rect=pg.Rect(x, y, size[0], size[1]), 
            text='Enter', 
            text_color=(255,255,255), 
            color=(150,150,150), 
            text_size=36
        )
        self.on_click = on_click
    
    def on_click(self):
        self.on_click()