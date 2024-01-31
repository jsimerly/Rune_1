from __future__ import annotations
import pygame as pg
from settings import BGCOLOR
from .draft_buttons import draft_icons, DraftIcon, LockInButton
from .drafted_characeter import DraftedCharacter, BannedCharacter
from .character_preview import draft_previews, CharacterPreview
from typing import TYPE_CHECKING, List, Dict

if TYPE_CHECKING:
    from drafting.client_state import DraftingState

class DraftUI:
    def __init__(self, n_picks:int, n_bans:int, draft_state: DraftingState) -> None:
        self.n_picks = n_picks
        self.n_bans = n_bans
        self.draft_state = draft_state
   
        self.draft_icons: List[DraftIcon] = []
        self.icon_map: Dict[str, DraftIcon] = {}

        self.team_1_bans: List[BannedCharacter] = []
        self.team_2_bans: List[BannedCharacter] = []
        self.team_1_picks: List[DraftedCharacter] = []
        self.team_2_picks: List[DraftedCharacter] = []
        self.lock_in_button: LockInButton = LockInButton((750, 900), not self.draft_state.my_turn)
        self.previews_map: Dict[str, CharacterPreview] = {}

        self.create_icons()
        self.create_pick_bans()
        self.create_previews()

        self.ui_elements = self.draft_icons + self.team_1_bans + self.team_1_picks + self.team_2_bans + self.team_2_picks 
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
            self.icon_map[icon.character_name] = icon

    def create_pick_bans(self):
        y_pos = 150
        my_pos = (100, y_pos)
        opp_pos = (1550, y_pos)

        for _ in range(self.n_bans):
            my_ban = BannedCharacter(position=my_pos)
            opp_ban = BannedCharacter(position=opp_pos)
            if self.draft_state.is_team_1:
                self.team_1_bans.append(my_ban)
                self.team_2_bans.append(opp_ban)
            else:
                self.team_2_bans.append(my_ban)
                self.team_1_bans.append(opp_ban)     

            my_pos = (my_pos[0], my_pos[1] + 155)
            opp_pos = (opp_pos[0], opp_pos[1] + 155)

        for _ in range(self.n_picks):
            my_pick = DraftedCharacter(my_pos)
            opp_pick = DraftedCharacter(opp_pos)
            if self.draft_state.is_team_1:
                self.team_1_picks.append(my_pick)
                self.team_2_picks.append(opp_pick)
            else:
                self.team_2_picks.append(my_pick)
                self.team_1_picks.append(opp_pick)

            my_pos = (my_pos[0], my_pos[1] + 155)
            opp_pos = (opp_pos[0], opp_pos[1] + 155)

    def create_previews(self):
        pos = (400, 100)
        for CharacterPreview in draft_previews:
            preview = CharacterPreview(pos)
            self.previews_map[preview.name] = preview

    def select_character(self, character: str):
        self.selected_character = character

    def set_ban_icon(self,my_turn: bool, ban_pos: int, character_str: str):
        image = self.icon_map[character_str].image
        if my_turn:
            self.team_1_bans[ban_pos].set_image(image)
        else:
            self.team_2_bans[ban_pos].set_image(image)

    def get_clicked_element(self, pixel):
        for element in self.clickable_elements:
            if element.rect.collidepoint(pixel):
                return element
        return None
    
    def draw_current_selection_draft_icon(self, display: pg.Surface):
        if self.draft_state.current_selection in self.icon_map:
            icon = self.icon_map[self.draft_state.current_selection]
            icon.draw()
        

    def render(self, display: pg.Surface):
        display.fill(BGCOLOR)
        for element in self.ui_elements:
            if not isinstance(element, DraftIcon):
                element.draw(display)

        for icon in self.clickable_elements:
            is_banning = self.draft_state.phase.current_phase.ban
            icon.draw(display, is_banning)

        if self.draft_state.current_selection in self.previews_map:
            preview = self.previews_map[self.selected_character]
            preview.draw(display=display)
