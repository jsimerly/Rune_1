import pygame as pg
from settings import BGCOLOR
from .draft_buttons import draft_icons, DraftIcon, LockInButton
from .drafted_characeter import DraftedCharacter, BannedCharacter
from .character_preview import draft_previews, CharacterPreview
from typing import TYPE_CHECKING, List, Dict

class DraftUI:
    def __init__(self, n_picks:int, n_bans:int) -> None:
        self.n_picks = n_picks
        self.n_bans = n_bans
        self.is_banning = True

        self.draft_icons: List[DraftIcon] = []

        self.my_bans: List[BannedCharacter] = []
        self.opp_bans: List[BannedCharacter] = []
        self.my_picks: List[DraftedCharacter] = []
        self.opp_picks: List[DraftedCharacter] = []
        self.lock_in_button: LockInButton = LockInButton((750, 900))
        self.previews_map: Dict[str, CharacterPreview] = {}

        self.selected_character = None

        self.create_icons()
        self.create_pick_bans()
        self.create_previews()

        self.ui_elements = self.draft_icons + self.my_bans + self.my_picks + self.opp_bans + self.opp_picks 
        self.clickable_elements = self.draft_icons + [self.lock_in_button]

        
    def create_icons(self):
        left_x = 375
        x_pos = left_x
        y_pos = 550
        for Icon in draft_icons:
            icon = Icon((x_pos, y_pos))
            x_pos += icon.size[0] + 5
            if x_pos > 1350:
                x_pos = left_x
                y_pos += 155
            self.draft_icons.append(icon)

    def create_pick_bans(self):
        y_pos = 150
        my_pos = (100, y_pos)
        opp_pos = (1550, y_pos)

        for _ in range(self.n_bans):
            my_ban = BannedCharacter(position=my_pos)
            opp_ban = BannedCharacter(position=opp_pos)
            self.my_bans.append(my_ban)
            self.opp_bans.append(opp_ban)

            my_pos = (my_pos[0], my_pos[1] + 155)
            opp_pos = (opp_pos[0], opp_pos[1] + 155)

        for _ in range(self.n_picks):
            my_pick = DraftedCharacter(my_pos)
            opp_pick = DraftedCharacter(opp_pos)
            self.my_picks.append(my_pick)
            self.opp_picks.append(opp_pick)

            my_pos = (my_pos[0], my_pos[1] + 155)
            opp_pos = (opp_pos[0], opp_pos[1] + 155)

    def create_previews(self):
        pos = (400, 100)
        for CharacterPreview in draft_previews:
            preview = CharacterPreview(pos)
            self.previews_map[preview.name] = preview

    def select_character(self, character: str):
        self.selected_character = character

    def set_ban_icon(self, ban_pos: int, image: pg.Surface):
        ban_pos -= 1
        if ban_pos < len(self.my_bans):
            self.my_bans[ban_pos].set_image(image)

    def get_clicked_element(self, pixel):
        for element in self.clickable_elements:
            if element.rect.collidepoint(pixel):
                return element
        return None

    def render(self, display: pg.Surface):
        display.fill(BGCOLOR)
        for element in self.ui_elements:
            if not isinstance(element, DraftIcon):
                element.draw(display)

        for icon in self.clickable_elements:
            icon.draw(display, self.is_banning)

        if self.selected_character in self.previews_map:
            preview = self.previews_map[self.selected_character]
            preview.draw(display=display)
