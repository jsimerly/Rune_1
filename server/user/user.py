from __future__ import annotations
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from game.game import Game
    from websockets import WebSocketServerProtocol
    from drafting.draft import Draft
class User:
    def __init__(self, username: str, websocket):
        self.username: str = username
        self.websocket: WebSocketServerProtocol = websocket
        self.drafts: List[Draft] = []
        self.games: List[Game] = []

    def add_draft(self, draft: Draft):
        self.drafts.append(draft)

    def add_game(self, game: Game):
        self.games.append(game)

    def remove_game(self, game: Game):
        self.games.remove(game)

    def serialize(self):
        return {
            'username': self.username
        }

 

    
