import pygame as pg
from ui_objects.abs_ui_object import AbsButton
from typing import List, Type
from settings import LIGHT_GREY
import time


class LockInButton(AbsButton):
    def __init__(self, position) -> None:
        self.size = (300, 50)
        rect = pg.Rect(position, self.size)
        self.color = (240, 244, 250)
        self.text_color = (0, 0 ,0)
        self.font = pg.font.SysFont(None, 24)

        self.show_outline = False
        self.outline_start_time = None

        super().__init__(rect)

    def draw(self, display: pg.Surface):
        pg.draw.rect(display, (240, 244, 250), self.rect)     
        self.draw_text(display=display)
        
        if self.show_outline:
            pg.draw.rect(display, (0,0,0), self.rect, 2)

            if time.time() - self.outline_start_time > 0.15:
                self.show_outline = False


    def draw_text(self, display: pg.Surface):
        text_surface = self.font.render('Lock-In', True, self.text_color)
        point = self.rect.center
        text_pos = (point[0] - text_surface.get_width() // 2, point[1] - text_surface.get_height() // 2)
        display.blit(text_surface, text_pos)

    def on_click(self):
        print('ya')
        self.show_outline = True
        self.outline_start_time = time.time()



class DraftIcon(AbsButton):
    def __init__(self, position: (int, int), image_path:str, character_name:str):
        self.size = (150, 150)
        image = pg.image.load(image_path)
        self.image = pg.transform.scale(image, self.size)
        self.character_name: str = character_name
        rect = pg.Rect(position, self.size)
        self.is_selected = False #related to client selection
        self.is_picked_or_banned = False #this is an attribute related to server state
        super().__init__(rect)

    def select(self):
        self.is_selected = True

    def unselect(self):
        self.is_selected = False

    def picked_banned(self):
        self.is_picked_or_banned = True

    def draw(self, display: pg.Surface, is_banning=False):
        display.blit(self.image, self.rect)
        if self.is_selected:
            if is_banning:
                self.draw_banning(display)
            else:
                self.draw_selected(display)

        if self.is_picked_or_banned:
            self.draw_unpickable(display)

    def draw_selected(self, display: pg.Surface):
        pg.draw.rect(display, (240, 244, 250), self.rect, 8)

    def draw_banning(self, display: pg.Surface):
        #draws an X through a the icon
        p1 = (self.rect.topright[0] - 20, self.rect.topright[1] + 20)
        p2 = (self.rect.bottomleft[0] + 20, self.rect.bottomleft[1] - 20)
        pg.draw.line(display, (168, 10, 10), p1, p2, 16)
        pg.draw.rect(display, (168, 10, 10), self.rect, 8)


    def draw_unpickable(self, display: pg.Surface):
        #draws an X through a the icon
        p1 = (self.rect.topright[0], self.rect.topright[1])
        p2 = (self.rect.bottomleft[0], self.rect.bottomleft[1])
        pg.draw.line(display, (168, 10, 10), p1, p2, 16)

    def on_click(self):
        self.select()
        ...
        #select the character and the when they lock in it sends it to the opponent.


class AthleaDraftButton(DraftIcon):
    def __init__(self, position: (int, int)):
        super().__init__(
            position, 
            'drafting/gui/icons/athlea_icon.png', 
            'Athlea',
        )

class BiziDraftButton(DraftIcon):
    def __init__(self, position: (int, int)):
        super().__init__(
            position, 
            'drafting/gui/icons/bizi_icon.png', 
            'Bizi',
        )

class BolindaDraftButton(DraftIcon):
    def __init__(self, position: (int, int)):
        super().__init__(
            position, 
            'drafting/gui/icons/bolinda_icon.png', 
            'Bolinda',
        )

class CrudDraftButton(DraftIcon):
    def __init__(self, position: (int, int)):
        super().__init__(
            position, 
            'drafting/gui/icons/crud_icon.png', 
            'Crud',
        )

class EmilieDraftButton(DraftIcon):
    def __init__(self, position: (int, int)):
        super().__init__(
            position, 
            'drafting/gui/icons/emilie_icon.png', 
            'Emilie',
        )

class HercDraftButton(DraftIcon):
    def __init__(self, position: (int, int)):
        super().__init__(
            position, 
            'drafting/gui/icons/herc_icon.png', 
            'Herc',
        )

class JudyDraftButton(DraftIcon):
    def __init__(self, position: (int, int)):
        super().__init__(
            position, 
            'drafting/gui/icons/judy_icon.png', 
            'Judy',
        )

class KaneDraftButton(DraftIcon):
    def __init__(self, position: (int, int)):
        super().__init__(
            position, 
            'drafting/gui/icons/kane_icon.png', 
            'Athlea',
        )

class LuDraftButton(DraftIcon):
    def __init__(self, position: (int, int)):
        super().__init__(
            position, 
            'drafting/gui/icons/lu_icon.png', 
            'Herc',
        )

class NaviDraftButton(DraftIcon):
    def __init__(self, position: (int, int)):
        super().__init__(
            position, 
            'drafting/gui/icons/navi_icon.png', 
            'Navi',
        )

class PapaDraftButton(DraftIcon):
    def __init__(self, position: (int, int)):
        super().__init__(
            position, 
            'drafting/gui/icons/papa_icon.png', 
            'Papa',
        )

class TimDraftButton(DraftIcon):
    def __init__(self, position: (int, int)):
        super().__init__(
            position, 
            'drafting/gui/icons/tim_icon.png', 
            'Papa',
        )

draft_icons: List[Type[DraftIcon]] = [
    AthleaDraftButton,
    BiziDraftButton,
    BolindaDraftButton,
    CrudDraftButton,
    EmilieDraftButton,
    HercDraftButton,
    JudyDraftButton,
    KaneDraftButton,
    LuDraftButton,
    NaviDraftButton,
    PapaDraftButton,
    TimDraftButton,
]