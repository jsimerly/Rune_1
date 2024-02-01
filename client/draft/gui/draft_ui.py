from __future__ import annotations
from typing import TYPE_CHECKING, List, Dict
import pygame as pg
from settings import BGCOLOR
from mouse_inputs import MouseInput, Click, DragEnd
from .buttons import LockInButton, DraftIcon
from .selected_boxes import DraftBox
from .preview import CharacterPreview, draft_previews

if TYPE_CHECKING:
    from draft.draft_state import DraftState
    from ui_objects.abs_ui_object import AbsButton, UIObject

class DraftUI:
    def __init__(self, state: DraftState):
        self.state: DraftState = state
        self.icons: List[DraftIcon] = []

        self.buttons: List[AbsButton] = []
        self.buttons.append(LockInButton((750, 900), self.state))

        self.my_bans: List[DraftBox] = []
        self.opp_bans: List[DraftBox] = []
        self.my_picks: List[DraftBox] = []
        self.opp_picks: List[DraftBox] = []
        self.previews_map: Dict[str, CharacterPreview] = {}

        self.add_icons()
        self.add_draft_boxes()
        self.add_previews()
        
        self.ui_elements: List[UIObject] = self.my_bans + self.opp_bans + self.my_picks + self.opp_picks

    def get_current_box(self) -> DraftBox:
        #includes if you're actively picking
        next_turn = self.state.phase.get_client_next_phase()
        if next_turn:
            if next_turn.is_ban:
                return self.my_bans[next_turn.pick-1]
            return self.my_picks[next_turn.pick-1]
        
    def add_icons(self):   
        left_x = 375
        x_pos = left_x
        y_pos = 550  

        for character in self.state.character_pool:
            pos = (x_pos, y_pos)
            x_pos += DraftIcon.size[0] + 5
            
            if x_pos > 1350:
                x_pos = left_x
                y_pos += 155
            icon = DraftIcon(pos, character)
   
            self.icons.append(icon)
            self.buttons.append(icon)


    def add_draft_boxes(self):
        y_pos = 150
        my_pos = (100, y_pos)
        opp_pos = (1550, y_pos)

        for _ in range(self.state.phase.n_bans):
            my_ban = DraftBox(pos=my_pos, is_ban=True)
            opp_ban = DraftBox(pos=opp_pos, is_ban=True)
            self.my_bans.append(my_ban)  
            self.opp_bans.append(opp_ban)

            my_pos = (my_pos[0], my_pos[1] + 155)
            opp_pos = (opp_pos[0], opp_pos[1] + 155)

        for _ in range(self.state.phase.n_picks):
            my_pick = DraftBox(pos=my_pos)
            opp_pick = DraftBox(pos=opp_pos)
            self.my_picks.append(my_pick)
            self.opp_picks.append(opp_pick)

            my_pos = (my_pos[0], my_pos[1] + 155)
            opp_pos = (opp_pos[0], opp_pos[1] + 155)

    def add_previews(self):
        pos = (400, 100)
        for CharacterPreview in draft_previews:
            preview_obj = CharacterPreview(pos)
            self.previews_map[preview_obj.name] = preview_obj

    def set_ban_box_image(self, my_team:bool, icon_image: pg.Surface):
        index = self.state.phase.current_phase.pick-1
        if my_team:
            self.my_bans[index].image = icon_image
        else:
            self.opp_bans[index].image = icon_image

    def set_pick_box_image(self, my_team: bool, icon_image: pg.Surface):
        index = self.state.phase.current_phase.pick -1
        if my_team:
            self.my_picks[index].image = icon_image
        else:
            self.opp_picks[index].image = icon_image
        
    def find_clicked_object(self, input: MouseInput):
        if isinstance(input, Click) or isinstance(input, DragEnd):
            for button in self.buttons:
                if button.rect.collidepoint(input.pixel):
                    button.on_click()
                    return button
        return None

    def render(self, display: pg.Surface):
        display.fill(BGCOLOR)
        for button in self.buttons:
            button.draw(display)

        for element in self.ui_elements:
            element.draw(display)

        current_box = self.get_current_box()
        if self.state.current_selection and current_box:
            current_box.image = self.state.current_selection.icon_image

        if self.state.current_selection:
            if self.state.current_selection.name in self.previews_map:
                preview = self.previews_map[self.state.current_selection.name]
                preview.draw(display)