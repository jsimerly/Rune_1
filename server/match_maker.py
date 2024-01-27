from __future__ import annotations
from typing import Protocol, TYPE_CHECKING, Tuple, Optional
import asyncio
from uuid import uuid4, UUID
from game.game_factory import GameFactory
from drafting.draft_factory import DraftFactory
import json

if TYPE_CHECKING:
    from user.user import User
    from drafting.draft import Draft

class MatchMaking:
    def __init__(self) -> None:
        self.user_1 = None
        self.user_2 = None
        self.draft_factory = DraftFactory()

    def add_to_queue(self, user: User) -> Optional[Draft]:
        if not self.user_1:
            self.user_1 = user
        else:
            self.user_2 = user
        
        if self.user_1 and self.user_2:
            draft_info = self.start_draft(self.user_1, self.user_2)
            self.user_1 = None
            self.user_2 = None
            return draft_info

        return None
    
    def start_draft(self, user_1: User, user_2: User) -> Draft:
        print(f'Starting a draft between {user_1.username} vs {user_2.username}')
        # return serializered game information here including the uuid and opponent.
        draft_obj = self.draft_factory.create(user_1, user_2)
        return draft_obj

    def notify_players_of_draft(self, draft_obj: Draft):
        #serializer draft here
        draft_obj
        package = json.dumps(draft_obj)
        user_1 = draft_obj.team_1.user
        if user_1.websocket.open:    
            asyncio.create_task(user_1.websocket.send(package))

        user_2 = draft_obj.team_2.user
        if user_2.websocket.open:
            asyncio.create_task(user_2.websocket.send(package))


