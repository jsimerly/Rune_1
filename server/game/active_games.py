from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from game.game import Game

class Games:
    def __init__(self) -> None:
        self.games: List[Game] = []