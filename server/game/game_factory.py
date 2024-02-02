from __future__ import annotations
from uuid import uuid4
import random
from game.game import Game
from map.maps.map_list import map_options
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from drafting.draft_team import DraftTeam

class GameFactory:
    def create_game(self, team_1: DraftTeam, team_2: DraftTeam):
        map_loadout = self.get_map()
        return Game(team_1=team_1, team_2=team_2, map=map_loadout)

    def get_map(self):
        #this actually needs to be moved to the draft at some point, we only have 1 map though.
        map_loudout = random.choice(map_options)
        return map_loudout



