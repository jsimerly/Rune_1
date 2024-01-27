from enum import Enum
from typing import List
from api.client_socket import TCPClient
from user.user import User

class DraftManager:
    def __init__(self, n_picks:int, n_bans:int, characters: List[str], phase, is_team_1: bool) -> None:
        self.characters = characters
        self.n_picks = n_picks
        self.n_ban = n_bans
        self.is_team_1 = is_team_1
        
        self.selected_character = None
        self.my_turn = True

        self.team_1_bans = []
        self.team_2_bans = []
        self.team_1_picks = []
        self.team_2_picks = []

        self.phase = phase
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





    