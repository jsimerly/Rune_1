import pygame as pg
from ui_objects.abs_ui_object import AbsButton
from typing import List, Type

class DraftIcon(AbsButton):
    def __init__(self, position: (int, int), image_path:str, character_name:str):
        self.size = (150, 150)
        image = pg.image.load(image_path)
        self.image = pg.transform.scale(image, self.size)
        self.character_name: str = character_name
        rect = pg.Rect(position, self.size)
        super().__init__(rect)

    def draw(self, display: pg.Surface):
        display.blit(self.image, self.rect)

    def on_click(self):
        ...
        #select the character and the when they lock in it sends it to the opponent.


class AthleaDraftButton(DraftIcon):
    def __init__(self, position: (int, int)):
        super().__init__(
            position, 
            'drafting/gui/icons/athlea_draft_icon.png', 
            'Athlea',
        )

class BiziDraftButton(DraftIcon):
    def __init__(self, position: (int, int)):
        super().__init__(
            position, 
            'drafting/gui/icons/bizi_draft_icon.webp', 
            'Bizi',
        )

class BolindaDraftButton(DraftIcon):
    def __init__(self, position: (int, int)):
        super().__init__(
            position, 
            'drafting/gui/icons/bolinda_drafting_icon.png', 
            'Bolinda',
        )

class CrudDraftButton(DraftIcon):
    def __init__(self, position: (int, int)):
        super().__init__(
            position, 
            'drafting/gui/icons/crud_draft_icon.png', 
            'Crud',
        )

class EmilieDraftButton(DraftIcon):
    def __init__(self, position: (int, int)):
        super().__init__(
            position, 
            'drafting/gui/icons/emilie_draft_icon.webp', 
            'Emilie',
        )

class HercDraftButton(DraftIcon):
    def __init__(self, position: (int, int)):
        super().__init__(
            position, 
            'drafting/gui/icons/herc_drafting_icon.png', 
            'Herc',
        )

class JudyDraftButton(DraftIcon):
    def __init__(self, position: (int, int)):
        super().__init__(
            position, 
            'drafting/gui/icons/judy_draft_icon.webp', 
            'Judy',
        )

class KaneDraftButton(DraftIcon):
    def __init__(self, position: (int, int)):
        super().__init__(
            position, 
            'drafting/gui/icons/kane_drafting_icon.png', 
            'Athlea',
        )

class LuDraftButton(DraftIcon):
    def __init__(self, position: (int, int)):
        super().__init__(
            position, 
            'drafting/gui/icons/lu_draft_icon.png', 
            'Herc',
        )

class NaviDraftButton(DraftIcon):
    def __init__(self, position: (int, int)):
        super().__init__(
            position, 
            'drafting/gui/icons/navi_draft_icon.png', 
            'Navi',
        )

class PapaDraftButton(DraftIcon):
    def __init__(self, position: (int, int)):
        super().__init__(
            position, 
            'drafting/gui/icons/papa_draft_icon.png', 
            'Papa',
        )

class TimDraftButton(DraftIcon):
    def __init__(self, position: (int, int)):
        super().__init__(
            position, 
            'drafting/gui/icons/tim_draft_icon.png', 
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