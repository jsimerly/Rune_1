from __future__ import annotations
from typing import Protocol, TYPE_CHECKING, Tuple, Optional
import asyncio
from uuid import uuid4, UUID
from game.game_factory import GameFactory

if TYPE_CHECKING:
    from user.user import User


class MatchMaking:
    def __init__(self) -> None:
        self.user_1 = None
        self.user_2 = None
        self.game_factory = GameFactory()

    def register_team(self, user: User) -> Tuple[Optional[UUID], Optional[User], Optional[User]]:
        if not self.user_1:
            self.user_1 = user
        else:
            self.user_2 = user
        
        if self.user_1 and self.user_2:
            game_info = self.start_game(self.user_1, self.user_2)
            return game_info
        return None

    def start_game(self, user_1: User, user_2: User):
        game = self.game_factory.create(user_1=user_1, user_2=user_2)
        print(f'Starting game between {user_1.username} vs {user_2.username}')
        self.user_1 = None
        self.user_2 = None
        # return serializered game information here including the uuid and opponent.
        game_id = game.uuid
        game_info = {
            'game_id': game_id,
            'user_1' : user_1,
            'user_2' : user_2
        }

        return game_info