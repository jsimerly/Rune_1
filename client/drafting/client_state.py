from client_state_proto import ClientState
from .gui.draft_icons import draft_icons, DraftIcon
from mouse_inputs import Click, DragEnd, MouseInput
from typing import List
import pygame as pg
from settings import BGCOLOR

class DraftingState(ClientState):
    def __init__(self, draft_id: str, opponent: str) -> None:
        self.draft_id = draft_id
        self.opponent = opponent
        self.character_icons: List[DraftIcon] = []
        self.create_icons()
        self.selected_character = None
    
    def render(self, display: pg.Surface):
        display.fill(BGCOLOR)
        self.draw_icons(display)

    def create_icons(self):
        x_pos = 300
        y_pos = 300
        for Icon in draft_icons:
            icon = Icon((x_pos, y_pos))
            x_pos += icon.size[0] + 5
            if x_pos > 1200:
                x_pos = 300
                y_pos += 155
            self.character_icons.append(icon)

    def draw_icons(self, display: pg.Surface):
        for icon in self.character_icons:
            icon.draw(display)

    def mouse_input(self, input: MouseInput):
        if isinstance(input, Click) or isinstance(input, DragEnd):
            self.check_for_icon_collision(input.pixel)

    def check_for_icon_collision(self, pixel_pos: (int,int)):
        for icon in self.character_icons:
            if icon.rect.collidepoint(pixel_pos):
                icon.on_click()

