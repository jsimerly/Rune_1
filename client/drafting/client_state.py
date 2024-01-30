from client_state_proto import ClientState
from .gui.draft_buttons import draft_icons, DraftIcon
from mouse_inputs import Click, DragEnd, MouseInput
from typing import Dict, List
import pygame as pg
from settings import BGCOLOR
from .draft_manager import DraftManager
from .gui.draft_ui import DraftUI, DraftIcon, LockInButton
from .draft_team import DraftTeam
from user.user import User
from drafting.draft_phase import DraftPhase
from api.client_socket import TCPClient

class DraftingState(ClientState): #Controller
    def __init__(self, draft_data: Dict) -> None:
        self.draft_id = draft_data['draft_id']
        self.team_1 = DraftTeam(draft_data['team_1']['team_id'])
        self.team_2 = DraftTeam(draft_data['team_2']['team_id'])

        self.user = User()
        self.is_team_1 = draft_data['team'] == 1
        self.my_team = self.team_1 if self.is_team_1 else self.team_2

        self.phase = DraftPhase.TEAM_1_BAN_1
        self.draft_manager = DraftManager(
            n_picks=3, 
            n_bans=1, 
            characters=[], 
            is_team_1 = self.is_team_1,
            phase=self.phase
        )
        self.draft_ui = DraftUI(
            n_picks=3, n_bans=1, phase=self.phase, is_team_1 = self.is_team_1
        )
        self.socket = TCPClient()
    
    def render(self, display: pg.Surface):
        self.draft_ui.render(display)

    def mouse_input(self, input: MouseInput):
        if isinstance(input, Click) or isinstance(input, DragEnd):
            element = self.draft_ui.get_clicked_element(input.pixel)
            if element:
                if isinstance(element, DraftIcon):
                    for icon in self.draft_ui.draft_icons:
                        icon.unselect()
                    element.select()
                    self.draft_ui.select_character(element.character_name)
                    self.draft_manager.select_character(element.character_name)
                    
                    if self.draft_manager.my_turn:
                        if self.draft_manager.phase == 1:
                            print(1)
                        self.draft_ui.set_ban_icon(1, image=element.image)

                if isinstance(element, LockInButton):
                    element.on_click()
                    self.notify_of_ban('crud')

    def notify_of_ban(self, character):
        package_kwargs = {
            'type' : 'draft',
            'serialized_message' : {
                'draft_id': str(self.draft_id),
                'team_id': str(self.my_team.team_id),
                'pick_type': 'ban',
                'phase': self.phase.value,
                'selected_character' : character,
            },
            'user' : self.user
        }

        self.socket.send_message(**package_kwargs)

    def server_input(self, message: Dict):
        print(message)
        pass

    def next_phase(self):
        next_value = self.state.value + 1
        if next_value > len(DraftPhase):
            self.complete = True
            return
        self.state = DraftPhase(next_value)
