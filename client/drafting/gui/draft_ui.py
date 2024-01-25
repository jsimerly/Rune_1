import pygame as pg
from settings import BGCOLOR
from .draft_icons import draft_icons, DraftIcon
from .drafted_characeter import DraftedCharacter, BannedCharacter
from typing import TYPE_CHECKING, List

class DraftUI:
    def __init__(self, n_picks:int, n_bans:int) -> None:
        self.n_picks = n_picks
        self.n_bans = n_bans

        self.draft_icons: List[DraftIcon] = []
        self.create_icons()
        self.my_bans: List[BannedCharacter] = []
        self.opp_bans: List[BannedCharacter] = []
        self.my_picks: List[DraftedCharacter] = []
        self.opp_picks: List[DraftedCharacter] = []
        self.create_pick_bans()

        self.ui_elements = self.draft_icons + self.my_bans + self.my_picks + self.opp_bans + self.opp_picks
        
    def create_icons(self):
        x_pos = 450
        y_pos = 300
        for Icon in draft_icons:
            icon = Icon((x_pos, y_pos))
            x_pos += icon.size[0] + 5
            if x_pos > 1400:
                x_pos = 450
                y_pos += 155
            self.draft_icons.append(icon)

    def create_pick_bans(self):
        y_pos = 100
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

    def get_clicked_element(self, pixel):
        print(self.ui_elements)
        for element in self.ui_elements:
            if element.rect.collidepoint(pixel):
                return element
        return None

    def render(self, display: pg.Surface):
        display.fill(BGCOLOR)
        for icon in self.ui_elements:
            icon.draw(display)