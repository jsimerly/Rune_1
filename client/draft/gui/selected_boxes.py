import pygame as pg
from ui_objects.abs_ui_object import UIObject
from draft.draft_characters import DraftCharacter
from typing import TYPE_CHECKING, Optional

class DraftBox(UIObject):
    def __init__(self, pos: (int, int, int), is_ban:bool=False) -> None:
        self.size = (150, 150)
        self.rect = pg.Rect(pos, self.size)
        
        self.is_ban = is_ban        
        self.is_active = False
        self.is_next = False
        self.outline_color = (149, 220, 252)
        if self.is_ban:
            self.outline_color = (168, 10, 10)

        self.image = None

    def draw(self, display: pg.Surface):
        if self.image:
            display.blit(self.image, self.rect)
            
        #make this flashing maybe?
        if self.is_active:
            pg.draw.rect(display, self.outline_color, self.rect, 8)

        if self.is_next:
            pg.draw.rect(display, self.outline_color, self.rect, 6)
        
        if all([
            not self.is_active,
            not self.is_next,
        ]):
            pg.draw.rect(display, self.outline_color, self.rect, 3)