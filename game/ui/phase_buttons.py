from __future__ import annotations
from typing import TYPE_CHECKING, Callable
import pygame as pg
from game.clickable_obj import ClickableRectObj

#will need to add a team component
class PhaseButton(ClickableRectObj):
    SIZE = (150, 50)
    TEXT_FONT = ('Arial', 24)

    def __init__(self, 
        screen,
        pixel_pos: (int,int), 
        text: str, 
        color: (int, int, int), 
        border_color: (int, int, int), 
        on_click: Callable
    ):
        self.pos = pixel_pos
        self.text = text
        self.color = color
        self.border_color = border_color
        self.clicked_method= on_click
        self.rect = pg.Rect(self.pos, self.SIZE)
        self.screen = screen

    def draw(self):
        pg.draw.rect(self.screen, self.color, self.rect)
        pg.draw.rect(self.screen, self.border_color, self.rect, 2)
        font = pg.font.SysFont(*self.TEXT_FONT)
        text_surf = font.render(self.text, True, self.border_color)

        text_rect = text_surf.get_rect(center=self.rect.center)
        self.screen.blit(text_surf, text_rect)

    def on_click(self):
        self.clicked_method()