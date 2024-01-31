from client_state_proto import ClientState
from .gui.draft_buttons import draft_icons, DraftIcon
from mouse_inputs import Click, DragEnd, MouseInput
from typing import Dict, List, Set
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
        self.my_turn = self.is_team_1

        self.phase = DraftPhase(self.team_1, self.team_2)
        
        self.team_1_bans: Set = set()
        self.team_2_bans: Set = set()
        self.team_1_picks: Set = set()
        self.team_2_picks: Set = set()
        self.current_selection = None

        self.draft_ui = DraftUI(
            n_picks=3, n_bans=1, draft_state=self
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
                    self.current_selection = element.server_char_name
                    self.draft_ui.set_ban_icon(self.my_turn, 0, element.character_name)
                    self.draft_ui.select_character(element.character_name)
                  

                if isinstance(element, LockInButton):
                    element.on_click()
                    self.notify_of_ban(self.current_selection)

    def notify_of_ban(self, character):
        package_kwargs = {
            'type' : 'draft',
            'serialized_message' : {
                'draft_id': str(self.draft_id),
                'team_id': str(self.my_team.team_id),
                'pick_type': 'ban',
                'phase': self.phase.current_phase.pos,
                'selected_character' : character,
            },
            'user' : self.user
        }

        self.socket.send_message(**package_kwargs)

    def server_input(self, package: Dict):
        if package['pick_type'] == 'ban':
            char_name = package['character']
            team_id = package['team_id']

            if team_id == self.team_1.team_id:
                self.team_1_bans.add(char_name)
            elif team_id == self.team_2.team_id:
                self.team_2_bans.add(char_name)
            else:
                print('team_id does not match any of the drafting teams.')

