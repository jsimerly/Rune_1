from __future__ import annotations
from typing import TYPE_CHECKING, Set, Dict, List, Optional
from .character_pool import draft_pool_map
from uuid import uuid4
from server_socket import TCPServer
from .draft_team import DraftTeam, DraftPick, DraftBan
from drafting.draft_phase import DraftPhase
from utils import Timer
import asyncio
from game.game_factory import GameFactory

if TYPE_CHECKING:
    from server.drafting.draft_team import DraftTeam, DraftCharacter, DraftPick, DraftBan, AbsDraftSelection
    from user.user import User
    from game.game import Game

class Draft:
    def __init__(self, user_1: DraftTeam, user_2: DraftTeam) -> None:
        self.team_1: DraftTeam = DraftTeam(user_1)
        self.team_2: DraftTeam = DraftTeam(user_2)

        self.draft_id = str(uuid4())
        self.socket = TCPServer()

        self.available: Dict[str, DraftCharacter] = draft_pool_map.copy()
        self.total_pool: List[str] = []
        for name in draft_pool_map.keys():
            self.total_pool.append(name)
        
        self.banned: Set[DraftBan] = set()
        self.picked: Set[DraftPick] = set()

        self.team_1_timer = Timer(31)
        self.team_1_timer.start(self.notify_user_time_up, self.team_1.user)
        self.team_2_timer = Timer(31)

        self.phase = DraftPhase(self.team_1, self.team_2)
        self.complete = False # somewhat unessesarily unless we start storing drafts in a db


    def is_active_team(self, team_id: DraftTeam):
       return self.phase.current_phase.team.team_id == team_id
    
    def handle_from_client(self, user, data):
        print('---- draft data from client ----')
        #could verify user is owner of team to prevent hacking, but shuldn't be an issue
        team_id = data['team_id']
        character_str = data['selected_character']
        if self.is_valid_selection(team_id, character_str):
            if data['is_ban'] and self.phase.current_phase.is_ban:
                self.ban(team_id, character_str)
            else:
                self.pick(team_id, character_str)

    @property
    def active_team(self) -> DraftTeam:
        return self.phase.current_phase.team

    def verify_active_team(self, team_id: str):
        return str(team_id) == str(self.active_team.team_id)
    
    def verify_character_available(self, character_str):
        return character_str in self.available
    
    def is_valid_selection(self, team_id: str, character_str: str):
        if self.verify_active_team(team_id):
            if self.verify_character_available(character_str):
                return True
            return False
        return False
    
    def start_next_timer(self):
        if self.phase.current_phase:
            if self.phase.current_phase.team == self.team_1:
                self.team_1_timer.start(self.notify_user_time_up, self.team_1.user)
                self.team_2_timer.cancel()
            if self.phase.current_phase.team == self.team_2:
                self.team_2_timer.start(self.notify_user_time_up, self.team_2.user)
                self.team_1_timer.cancel()
        
        if self.phase.is_complete:
            self.team_1_timer.cancel()
            self.team_2_timer.cancel()

    def next_phase(self):
        is_complete = self.phase.next_phase()
        self.start_next_timer()
        
        if is_complete:
            self.start_game()

    def start_game(self):
        factory = GameFactory()
        game_obj = factory.create_game(self.team_1, self.team_2)
        self.notify_of_game_start(self.team_1.user, game_obj)
        self.notify_of_game_start(self.team_2.user, game_obj)

        ...

    def notify_of_game_start(self, user, game_obj: Game):
        message = {
            'draft_type': 'game_starting',
            'info': {
                **game_obj.serialize_info()
            }
        }
        self.socket.send_message(user, 'draft', message)

    def ban(self, team_id:str, character_str: str):
        character_obj = self.available[character_str]()
        del self.available[character_str]
        
        ban = DraftBan(self.active_team, character_obj)
        self.active_team.ban(ban)
        picking_team = self.team_1 if team_id == self.team_1.team_id else self.team_2
        picking_team.ban(ban)
        self.banned.add(ban)
        self.next_phase()

        user_1 = self.team_1.user
        user_2 = self.team_2.user
    
        self.notify_user_of_ban(user_1, ban)
        self.notify_user_of_ban(user_2, ban)

    def notify_user_of_ban(self, user: User, ban: DraftBan):
        message = {
            'draft_type': 'pick',
            'info':{            
                'pick_type': 'ban',
                'team_id': self.active_team.team_id,
                'character': ban.character.name,
                'pick': self.phase.current_phase.pick,
            }
        }
        self.socket.send_message(user, 'draft', message)
        ...

    def notify_user_time_up(self, user):
        message = {
            'draft_type': 'time_up',
            'info': {
                'message': 'TIMES UP'
            }
        }
        self.socket.send_message(user, 'draft', message)


    def pick(self, team_id:str, character_str: str):
        character_obj = self.available[character_str]()
        del self.available[character_str]
        pick = DraftPick(self.active_team, character_obj)

        picking_team = self.team_1 if team_id == self.team_1.team_id else self.team_2
        picking_team.pick(pick)
        self.picked.add(pick)
        self.next_phase()

        user_1 = self.team_1.user
        user_2 = self.team_2.user

        self.notify_user_of_pick(user_1, pick)
        self.notify_user_of_pick(user_2, pick)

    def notify_user_of_pick(self, user: User, pick: DraftPick):
        message = {
            'draft_type': 'pick',
            'info': {
                'pick_type': 'pick',
                'team_id': self.active_team.team_id,
                'character': pick.character.name,
                'pick': self.phase.current_phase.pick,
            }
        }

        self.socket.send_message(user, 'draft', message)


    ''' Serialization '''
    def serialize(self):
        return {
                'draft_id': str(self.draft_id),
                'team_1': self.team_1.serialize(),
                'team_2': self.team_2.serialize()
            }
        ...