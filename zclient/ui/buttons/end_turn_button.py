from typing import Callable
from .button import Button
import pygame as pg

pg.font.init()
font = pg.font.SysFont('Arial', 20)
class EndTurnButton(Button):
    def __init__(self):
        self.text = 'End Turn'
        self.is_disabled = False
        self.rect = pg.Rect(150, 800, 200, 62)

    def on_click(self):
        self.is_disabled = True
        self.text = 'Waiting on Other Player...'

    def draw(self, screen: pg.Surface):
        bg_color = (211, 211, 211)
        text_color = (40, 40, 40)
        if self.is_disabled:
            bg_color = (128, 128, 128)
            text_color = (150, 150, 150)

        pg.draw.rect(screen, bg_color, self.rect)
        text_surface = font.render(self.text, True, text_color)
        point = self.rect.center
        text_pos = (point[0] - text_surface.get_width() // 2, point[1] - text_surface.get_height() // 2)
        screen.blit(text_surface, text_pos)

        