from __future__ import annotations
from drafting.draft import Draft
from drafting.draft_team import DraftTeam
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from user.user import User

class DraftFactory:
    def create(self, user_1: User, user_2: User):
        return Draft(user_1=user_1, user_2= user_2)
    
    def get_map(self):
        return "map_1"
