from client_state_proto import ClientState
from .gui.draft_icons import draft_icons, DraftIcon
from mouse_inputs import Click, DragEnd, MouseInput
from typing import Dict, List
import pygame as pg
from settings import BGCOLOR
from .draft_manager import DraftManager
from .gui.draft_ui import DraftUI, DraftIcon

class DraftingState(ClientState): #Controller
    def __init__(self, draft_id: str, opponent: str) -> None:
        self.draft_id = draft_id
        self.opponent = opponent
        self.draft_manager = DraftManager(n_picks=3, n_bans=1, characters=[])
        self.draft_ui = DraftUI(n_picks=3, n_bans=1)
    
    def render(self, display: pg.Surface):
        self.draft_ui.render(display)

    def mouse_input(self, input: MouseInput):
        if isinstance(input, Click) or isinstance(input, DragEnd):
            print(1)
            element = self.draft_ui.get_clicked_element(input.pixel)
            if element:
                print(2)
                if isinstance(element, DraftIcon):
                    for icon in self.draft_ui.draft_icons:
                        icon.unselect()
                    print(3)
                    element.select()

    def server_input(self, message: Dict):
        pass

