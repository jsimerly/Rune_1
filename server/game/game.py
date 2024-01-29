from typing import TYPE_CHECKING
from .states.game_state import InGameState
from .states.drafting_state import DraftingState
from .states.abs_state import AbstactGameState

if TYPE_CHECKING:
    from user.user import User
    
class Game:
    def __init__(self, map, uuid, user_1, user_2) -> None:
        self.map = map
        self.game_id = uuid
        self.user_1: User = user_1
        self.user_2: User = user_2
        # self.team_1 = Team(user=user_1)
        # self.team_2 = Team(user=user_2)
        self.state: AbstactGameState = DraftingState(self.on_drafting_complete)
        self.round = 1

    def on_drafting_complete(self):
        self.state = InGameState(self.on_game_complete)

    def on_game_complete(self):
        print('handle game cleanup')
