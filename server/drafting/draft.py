from __future__ import annotations
from typing import TYPE_CHECKING, Set, Dict, List, Optional
from .character_pool import draft_pool_map
from uuid import uuid4
from enum import Enum
import json
from server_socket import TCPServer
from .draft_team import DraftTeam, DraftPick, DraftBan

if TYPE_CHECKING:
    from server.drafting.draft_team import DraftTeam, DraftCharacter, DraftPick, DraftBan, AbsDraftSelection
    
class DraftPhase(Enum):
    TEAM_1_BAN_1 = 1
    TEAM_2_BAN_1 = 2
    TEAM_1_PICK_1 = 3
    TEAM_2_PICK_1 = 4
    TEAM_2_PICK_2 = 5
    TEAM_1_PICK_2 = 6
    TEAM_1_PICK_3 = 7
    TEAM_2_PICK_3 = 8
    COMPLETED = 9

class Draft:
    def __init__(self, user_1: DraftTeam, user_2: DraftTeam) -> None:
        self.team_1: DraftTeam = DraftTeam(user_1)
        self.team_2: DraftTeam = DraftTeam(user_2)
        self.active_team = self.team_1

        self.draft_id = str(uuid4())
        self.socket = TCPServer()

        self.available: Dict[str, DraftCharacter] = draft_pool_map
        self.total_pool: List[str] = []
        for name in draft_pool_map.keys():
            self.total_pool.append(name)
        
        self.banned: Set[DraftBan] = set()
        self.picked: Set[DraftPick] = set()

        self.phase = DraftPhase.TEAM_1_BAN_1
        self.complete = False # somewhat unessesarily unless we start storing drafts in a db

    def next_phase(self):
        next_value = self.state.value + 1
        if next_value > len(DraftPhase):
            self.complete = True
            return
        self.state = DraftPhase(next_value)

    def is_active_team(self, team_id: DraftTeam):
        team_1_turns = [
            DraftPhase.TEAM_1_BAN_1, DraftPhase.TEAM_1_PICK_1, 
            DraftPhase.TEAM_1_PICK_2,DraftPhase.TEAM_1_PICK_3
        ]
        team_2_turns = [
            DraftPhase.TEAM_2_BAN_1, DraftPhase.TEAM_2_PICK_1, 
            DraftPhase.TEAM_2_PICK_2,DraftPhase.TEAM_2_PICK_3
        ]

        if self.phase in team_1_turns:
            return str(self.team_1.team_id) == team_id
        
        if self.phase in team_2_turns:
            return str(self.team_2.team_id) == team_id
        return False
    
    def handle_from_client(self, user, data):
        print('---- draft data from clinet ----')
        #could verify user is owner of team to prevent hacking, but shuldn't be an issue
        team_id = data['team_id']
        character_str = data['selected_character']
        if self.is_valid_selection(team_id, character_str):
            pick_type = data['pick_type']
            if pick_type == 'ban':
                self.ban(character_str)
                print(self.banned)
            if pick_type == 'pick':
                self.pick(character_str)
                print(self.picked)

        
            #handle next phase and response

        ...
    def notifiy_user_of_ban(self, user):
        message = {}
        self.socket.send_message(user)
        ...

    def verify_active_team(self, team_id: str):
        return str(team_id) == str(self.active_team.team_id)
    
    def verify_character_available(self, character_str):
        return character_str in self.available
    
    def is_valid_selection(self, team_id: str, character_str: str):
        if self.verify_active_team(team_id):
            if self.verify_character_available(character_str):
                return True

            #handle not available
            return False
        #handle wrong team error
        return False


    def ban(self, character_str: str):
        character_obj = self.available[character_str]()
        del self.available[character_str]
        
        ban = DraftBan(self.active_team, character_obj)
        self.active_team.ban(ban)
        self.banned.add(ban)


    def pick(self, team_id: str, character_str: str):
        if self.is_valid_selection(team_id, character_str):
            character_obj = self.available[character_str]()
            del self.available[character_str]
            
            ban = DraftPick(character_obj)
            self.team_1.pick(ban)
            self.picked.add(ban)

    def notify_of_ban(self, selection: AbsDraftSelection):
        package = json.dumps({
            'type': 'draft',
            'data': {
                **selection.serialize(),
                'phase': self.phase.value,
            }
        })

        self.socket.send_message(self.team_1.user, package)
        self.socket.send_message(self.team_2.user, package) 
        ...

    def notify_of_pick(self, pick: DraftPick):
        ...

    ''' Serialization '''
    def serialize(self):
        return {
                'draft_id': str(self.draft_id),
                'team_1': self.team_1.serialize(),
                'team_2': self.team_2.serialize()
            }
        ...