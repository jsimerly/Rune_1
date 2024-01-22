from uuid import uuid4
import random
from game.game import Game
from map.maps.map_list import map_options

class GameFactory:
    def create(self, user_1, user_2):
        map_loadout = self.get_map()
        return Game(map=map_loadout, uuid=uuid4(), user_1=user_1, user_2=user_2)

    def get_map(self):
        map_loudout = random.choice(map_options)
        return map_loudout



