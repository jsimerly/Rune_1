from ui_objects.abs_ui_object import AbsButton
import pygame as pg
import time
from typing import List, Type, Optional
from draft.draft_characters import *


class LockInButton(AbsButton):
    def __init__(self, position, clickable=True) -> None:
        self.clickable = clickable
        self.size = (300, 50)
        rect = pg.Rect(position, self.size)
        self.color = (240, 244, 250)
        self.text_color = (0, 0 ,0)
        self.font = pg.font.SysFont(None, 24)

        self.show_outline = False
        self.outline_start_time = None

        super().__init__(rect)

    def draw(self, display: pg.Surface, is_ban:bool = False):
        text = 'Ban' if is_ban else 'Pick'
        bg_color = (240, 244, 250) if self.clickable else (100, 100, 100)
        pg.draw.rect(display, bg_color, self.rect)     
        self.draw_text(display=display, text=text)
        
        if self.show_outline:
            pg.draw.rect(display, (0,0,0), self.rect, 2)

            if time.time() - self.outline_start_time > 0.15:
                self.show_outline = False

    def draw_text(self, display: pg.Surface, text=None):
        if text == None:
            text = 'Lock-In'

        text_color = self.text_color if self.clickable else (75, 75, 75)
        text_surface = self.font.render(text, True, text_color)
        point = self.rect.center
        text_pos = (point[0] - text_surface.get_width() // 2, point[1] - text_surface.get_height() // 2)
        display.blit(text_surface, text_pos)

    def on_click(self):
        if self.clickable:
            self.show_outline = True
            self.outline_start_time = time.time()

class DraftIcon(AbsButton):
    size = (150, 150)

    def __init__(self, pos:(int,int), draft_character: DraftCharacter):
        rect = pg.Rect(pos, self.size)
        self.pos = pos
        self.character = draft_character
        super().__init__(rect)

    def draw(self, display: pg.Surface):
        display.blit(self.character.icon_image, self.rect)

        if self.character.is_banned:
            self.draw_banned(display)

        if self.character.is_selected:
            self.draw_selected(display)

        if self.character.is_picked:
            self.draw_unpickable(display)

        if self.character.is_banning:
            self.draw_banning(display)

    def draw_selected(self, display: pg.Surface):
        pg.draw.rect(display, (240, 244, 250), self.rect, 8)

    def draw_banned(self, display: pg.Surface):
        p1 = (self.rect.topright[0] - 20, self.rect.topright[1] + 20)
        p2 = (self.rect.bottomleft[0] + 20, self.rect.bottomleft[1] - 20)
        pg.draw.line(display, (168, 10, 10), p1, p2, 16)

    def draw_banning(self, display: pg.Surface):
        p1 = (self.rect.topright[0] - 20, self.rect.topright[1] + 20)
        p2 = (self.rect.bottomleft[0] + 20, self.rect.bottomleft[1] - 20)
        pg.draw.line(display, (168, 10, 10), p1, p2, 16)
        pg.draw.rect(display, (168, 10, 10), self.rect, 8)

    def draw_unpickable(self, display: pg.Surface):
        p1 = (self.rect.topright[0], self.rect.topright[1])
        p2 = (self.rect.bottomleft[0], self.rect.bottomleft[1])
        pg.draw.line(display, (240, 244, 250), p1, p2, 16)

    def on_click(self):
        return super().on_click()


class AthleaDraftButton(DraftIcon):
    def __init__(self, position: (int, int)):
        super().__init__(position, Athlea_DraftCharacter())

class BiziDraftButton(DraftIcon):
    def __init__(self, position: (int, int)):
        super().__init__(position, Bizi_DraftCharacter())

class BolindaDraftButton(DraftIcon):
    def __init__(self, position: (int, int)):
        super().__init__(position, Bolinda_DraftCharacter())

class CrudDraftButton(DraftIcon):
    def __init__(self, position: (int, int)):
        super().__init__(position, Crud_DraftCharacter())

class EmilyDraftButton(DraftIcon):
    def __init__(self, position: (int, int)):
        super().__init__(position, Emily_DraftCharacter())

class HercDraftButton(DraftIcon):
    def __init__(self, position: (int, int)):
        super().__init__(position, Herc_DraftCharacter())

class IvanDraftButton(DraftIcon):
    def __init__(self, position: (int, int)):
        super().__init__(position, Ivan_DraftCharacter())

class JudyDraftButton(DraftIcon):
    def __init__(self, position: (int, int)):
        super().__init__(position, Judy_DraftCharacter())

class KaneDraftButton(DraftIcon):
    def __init__(self, position: (int, int)):
        super().__init__(position, Kane_DraftCharacter())

class LuDraftButton(DraftIcon):
    def __init__(self, position: (int, int)):
        super().__init__(position, Lu_DraftCharacter())

class NaviDraftButton(DraftIcon):
    def __init__(self, position: (int, int)):
        super().__init__(position, Navi_DraftCharacter())

class PapaDraftButton(DraftIcon):
    def __init__(self, position: (int, int)):
        super().__init__(position, Papa_DraftCharacter())

class TimDraftButton(DraftIcon):
    def __init__(self, position: (int, int)):
        super().__init__(position, Tim_DraftCharacter())

draft_icons: List[Type[DraftIcon]] = [
    AthleaDraftButton,
    BiziDraftButton,
    BolindaDraftButton,
    CrudDraftButton,
    EmilyDraftButton,
    HercDraftButton,
    IvanDraftButton,
    JudyDraftButton,
    KaneDraftButton,
    LuDraftButton,
    NaviDraftButton,
    PapaDraftButton,
    TimDraftButton,
]