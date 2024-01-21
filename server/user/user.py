from server.game.game import Game
from typing import TYPE_CHECKING, List

class User:
    def __init__(self, username: str, websocket):
        self.username = username
        self.websocket = websocket
        self.games: List[Game] = []

    def add_game(self, game: Game):
        self.games.append(game)

    def remove_game(self, game: Game):
        self.games.remove(game)
 

    
