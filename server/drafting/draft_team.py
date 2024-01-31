from __future__ import annotations

from uuid import uuid4
from typing import Set, List, TYPE_CHECKING
from abc import ABC, abstractmethod 
import json

if TYPE_CHECKING:
    from user.user import User

class DraftCharacter:
    def __init__(self, name: str) -> None:
        self.name = name

class AbsDraftSelection(ABC):
    @abstractmethod
    def serialize(self):
        ...

class DraftBan(AbsDraftSelection):
    def __init__(self, team: DraftTeam, character: DraftCharacter) -> None:
        self.team = team
        self.character = character

    def serialize(self):
        return {
            'team_id': str(self.team.team_id),
            'draft_type': 'ban',
            'character_name': self.character.name  
        }
    

class DraftPick(AbsDraftSelection):
    def __init__(self, team: DraftTeam, character: DraftCharacter) -> None:
        self.team = team
        self.character =  character

    def serialize(self):
        return {
            'team_id': str(self.team.team_id),
            'draft_type': 'pick',
            'character_name': self.character.name  
        }

class DraftTeam:
    def __init__(self, user: User) -> None:
        self.user: User = user
        self.team_id = str(uuid4())
        self.bans: Set[DraftBan] = set()
        self.picks: Set[DraftPick] = set()

    def ban(self, ban: DraftBan):
        self.bans.add(ban)

    def pick(self, pick: DraftPick):
        self.picks.add(pick)

    ''' Serialization '''
    def serialize(self):
        return {
            'team_id': str(self.team_id),
            'bans': [ban.serialize() for ban in self.bans],
            'picks': [pick.serialize() for pick in self.picks]
        }
    