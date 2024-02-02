from __future__ import annotations
from typing import TYPE_CHECKING
from .states.game_state import InGameState
from .states.abs_state import AbstactGameState
from uuid import uuid4
from .team import Team

if TYPE_CHECKING:
    from user.user import User
    from drafting.draft_team import DraftTeam
    
class Game:
    def __init__(self, team_1: DraftTeam, team_2: DraftTeam, map) -> None:
        self.map = map
        self.game_id = str(uuid4())
        self.team_1 = Team(draft_team=team_1)
        self.team_2 = Team(draft_team=team_2)

        self.round = 1


    def serialize_info(self):
        return {
            'game_id': self.game_id,
            'team_1': self.team_1.serialize(),
            'team_2': self.team_2.serialize(),
            'round': self.round,
        }
    
    def serialize_game_state(self):
        ...


    #probably move gameplay processing to a component of Game
    def serialize_playout(self):
        ...
