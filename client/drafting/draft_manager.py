from enum import Enum
from typing import List
from api.client_socket import TCPClient
from user.user import User

class DraftPhase(Enum):
    BAN_1 = 1
    BAN_2 = 2
    TEAM_1_PICK_1 = 3
    TEAM_2_PICK_1_2 = 4
    TEAM_1_PICK_2_3 = 5
    TEAM_1_PICK_3 = 6
    COMPLETED = 7

class DraftManager:
    def __init__(self, n_picks:int, n_bans:int, characters: List[str]) -> None:
        self.characters = characters
        self.n_picks = n_picks
        self.n_ban = n_bans
        self.selected_character = None
        self.my_turn = True

        self.bans = []
        self.opponent_bans = []
        self.characters = []
        self.opponnent_characters = []

        self.phase = DraftPhase.BAN_1  
        self.socket = TCPClient()
        self.user = User()

    def _is_available(self, character: str):
        if character not in self.characters:
            raise ValueError('That character does not exist')
        
        if character in self.bans:
            return False
        
        if character in self.opponent_bans:
            return False

        if character in self.characters:
            return False
        
        if character in self.opponnent_characters:
            return False
        
        return True
    
    def select_character(self, character: str):
        self.selected_character = character
    
    def ban_character(self):
        if self._is_available(self.select_character):
            self.bans.append(self.selected_character)
            self.send_ban_message(self.selected_character)
            
        print('You cannot ban that character.')

    def send_ban_message(self, character: str):
        package_kwargs = {
            'type' : 'draft',
            'data' : {
                'pick_type': 'ban',
                'selected_character' : character,
            },
            'user' : self.user
        }

        self.socket.send_data(**package_kwargs)

    def next_phase(self):
        next_value = self.state.value + 1
        if next_value > len(DraftPhase):
            self.complete = True
            return
        self.state = DraftPhase(next_value)



    