from __future__ import annotations
from typing import TYPE_CHECKING
from uuid import uuid4

if TYPE_CHECKING:
    from user.user import User
    from drafting.draft_team import DraftTeam

class Team:
    def __init__(self, draft_team: DraftTeam) -> None:
        self.team_id = str(uuid4())
        self.user = draft_team.user
        self.turn_submitted = False
        self.characters = [] 
        self.buildings = []

    def serialize(self):
        return {
            'team_id': self.team_id,
            'user': self.user.serialize()
        }
