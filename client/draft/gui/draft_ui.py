from __future__ import annotations
from typing import TYPE_CHECKING, List
import pygame as pg
from settings import BGCOLOR
from mouse_inputs import MouseInput, Click, DragEnd
from .buttons import draft_icons, LockInButton, DraftIcon
from .selected_boxes import DraftBox

if TYPE_CHECKING:
    from draft.draft_state import DraftState
    from ui_objects.abs_ui_object import AbsButton, UIObject

class DraftUI:
    def __init__(self, state: DraftState):
        self.state: DraftState = state
        self.icons: List[DraftIcon] = []

        self.buttons: List[AbsButton] = []
        self.buttons.append(LockInButton((750, 900), self.state.phase.is_client_turn))

        self.my_bans: List[DraftBox] = []
        self.opp_bans: List[DraftBox] = []
        self.my_picks: List[DraftBox] = []
        self.opp_picks: List[DraftBox] = []

        self.add_icons()
        self.add_draft_boxes()
        
        self.ui_elements: List[UIObject] = self.my_bans + self.opp_bans + self.my_picks + self.opp_picks

    def get_current_box(self) -> DraftBox:
        if self.state.phase.is_client_turn:
            if self.state.phase.current_phase.is_ban:
                return self.my_bans[self.state.phase.current_phase.pick-1]
            return self.my_picks[self.state.phase.current_phase.pick-1]
        
        if self.state.phase.current_phase.is_ban:
            return self.opp_bans[self.state.phase.current_phase.pick-1]
        return self.opp_picks[self.state.phase.current_phase.pick-1]

    def add_icons(self):   
        left_x = 375
        x_pos = left_x
        y_pos = 550  

        for icon in draft_icons:
            pos = (x_pos, y_pos)
            x_pos += icon.size[0] + 5
            if x_pos > 1350:
                x_pos = left_x
                y_pos += 155
            
            icon_obj = icon(pos)
            self.icons.append(icon_obj)
            self.buttons.append(icon_obj)


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

    def set_ban_box_image(self, my_team:bool, icon_image: pg.Surface):
        index = self.state.phase.current_phase.pick-1
        if my_team:
            self.my_bans[index].image = icon_image
        else:
            self.opp_bans[index].image = icon_image

    def set_pick_box_image(self, index, my_team: bool, icon_image: pg.Surface):
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
        if self.state.current_selection:
            current_box.image = self.state.current_selection.icon_image