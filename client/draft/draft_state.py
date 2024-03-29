from client_state_proto import ClientState
from mouse_inputs import Click, DragEnd, MouseInput
from typing import Dict, List, Set, Optional
import pygame as pg
from settings import BGCOLOR
from user.user import User
from draft.draft_phase import DraftPhase
from api.client_socket import TCPClient
from draft.draft_team import DraftTeam, DraftBan, DraftPick
from draft.draft_characters import DraftCharacter
from .gui.draft_ui import DraftUI  
from draft.draft_characters import character_pool_cls_list
from .gui.buttons import DraftIcon, LockInButton
from utils import Timer

class DraftState(ClientState):
    def __init__(self, draft_data: Dict) -> None:
        self.user = User()
        self.socket = TCPClient()

        self.draft_id = draft_data['draft_id']
        team_1 = draft_data['team_1']
        team_2 = draft_data['team_2']

        self.team_1 = DraftTeam(team_1['team_id'], team_1['user']['username'])
        self.team_2 = DraftTeam(team_2['team_id'], team_2['user']['username'])
        self.client_team = self.team_1 if draft_data['team'] == 1 else self.team_2

        self.character_pool: List[DraftCharacter] = [
            char() for char in character_pool_cls_list
        ]
        self.phase = DraftPhase(self.team_1, self.team_2, self.client_team)

        self.team_1_bans: List[DraftBan] = [None for _ in range(self.phase.n_bans)]
        self.team_2_bans: List[DraftBan] = [None for _ in range(self.phase.n_bans)]
        self.team_1_picks: List[DraftPick] = [None for _ in range(self.phase.n_picks)]
        self.team_2_picks: List[DraftPick] = [None for _ in range(self.phase.n_picks)]
        self.current_selection: Optional[DraftCharacter] = None

        #really should add these to the DraftTeam class instead
        self.team_1_timer = Timer(30) #these values should come from server on init
        self.team_1_timer.start()
        self.team_2_timer = Timer(30)
        self.draft_ui = DraftUI(state=self)

    def mouse_input(self, mouse_input: MouseInput):
        element_clicked = self.draft_ui.find_clicked_object(mouse_input)
        if element_clicked:
            if isinstance(element_clicked, DraftIcon): #draft icon
                if self.current_selection:
                    self.current_selection.is_selected = False
                    self.current_selection.is_banning = False

                character = element_clicked.character
                self.current_selection = character
                character.is_selected = True


                if self.phase.current_phase and self.phase.current_phase.is_ban:
                    character.is_banning = True

            if isinstance(element_clicked, LockInButton):
                #check if it's event my turn to notify server
                if self.current_selection in self.character_pool:
                    if self.phase.is_client_turn:
                        self.notify_server_of_pick()
                    else:
                        print('It is not your turn.')

    def notify_server_of_pick(self):
        if self.current_selection:
            package_kwargs = {
                'type' : 'draft',
                'serialized_message': {
                    'draft_id': str(self.draft_id),
                    'team_id': str(self.client_team.team_id),
                    'is_ban': self.phase.current_phase.is_ban,
                    'phase': self.phase.current_phase.pick,
                    'selected_character' : self.current_selection.server_name,
                },
                'user': self.user
            }

            self.socket.send_message(**package_kwargs)
        else:
            print('There is no current selection.')

    def server_input(self, message: Dict):
        if message['draft_type'] == 'game_starting':
            game_info = message['info']
            print('game starting - draft_state')

        if message['draft_type'] == 'time_up':
            self.notify_server_of_pick()

        if message['draft_type'] == 'pick':
            pick_info = message['info']
            if pick_info['pick_type'] == 'ban':
                char_name = pick_info['character']
                team_id = pick_info['team_id']
                if team_id == self.team_1.team_id:
                    self.ban(self.team_1, char_name)
                elif team_id == self.team_2.team_id:
                    self.ban(self.team_2, char_name)
                else:
                    print('team_id does not match any of the drafting teams.')

                self.start_next_timer()

            if pick_info['pick_type'] == 'pick':
                pick_info = message['info']
                char_name = pick_info['character']
                team_id = pick_info['team_id']
                if team_id == self.team_1.team_id:
                    self.pick(self.team_1, char_name)
                elif team_id == self.team_2.team_id:
                    self.pick(self.team_2, char_name)
                else:
                    print('team_id does not match any of the drafting teams.')

                self.start_next_timer()
                

    def ban(self, team: DraftTeam, character_str: str):
        character_obj = self.pop_character_obj(character_str)
        character_obj.is_banned = True
    
        if self.team_1 == team:
            self.team_1_bans.append(character_obj)
            self.draft_ui.set_ban_box_image( 
                my_team=self.phase.is_client_turn,
                icon_image=character_obj.icon_image
            )
        else:
            self.team_2_bans.append(character_obj)
            self.draft_ui.set_ban_box_image(
                my_team=self.phase.is_client_turn,
                icon_image=character_obj.icon_image,
            )

        self.phase.next_phase()

    def pick(self, team: DraftTeam, character_str: str):
        character_obj = self.pop_character_obj(character_str)
        character_obj.is_picked = True
        if self.team_1 == team:
            self.team_1_picks.append(character_obj)
            self.draft_ui.set_pick_box_image(
                my_team=self.phase.is_client_turn,
                icon_image=character_obj.icon_image,
            )
        else:
            self.team_2_picks.append(character_obj)
            self.draft_ui.set_pick_box_image(
                my_team=self.phase.is_client_turn,
                icon_image=character_obj.icon_image,
            )
        self.phase.next_phase()

    def start_next_timer(self):
        if self.phase.current_phase:
            if self.phase.current_phase.team == self.team_1:
                self.team_1_timer.start()
                self.team_2_timer.cancel()
            if self.phase.current_phase.team == self.team_2:
                self.team_2_timer.start()
                self.team_1_timer.cancel()
        
        if self.phase.is_complete:
            self.team_1_timer.cancel()
            self.team_2_timer.cancel()
        

    def pop_character_obj(self, character_str: str) -> DraftCharacter:
        for i, character_draft_obj in enumerate(self.character_pool):
            if character_str == character_draft_obj.name:
                character_obj = self.character_pool.pop(i)
        return character_obj
    
    @property
    def current_selection_available(self):
        return self.current_selection in self.character_pool
                    
    def render(self, display: pg.Surface):
        self.draft_ui.render(display)

    

