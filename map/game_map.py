from .game_tile import GameTile
from .loadouts.map_layout import MapLayout

from hex import Point

class GameMap:
    def __init__(self, map: MapLayout, screen):
        self.tiles = map.generate_map(screen)
        self.screen = screen
        self.layout = map.layout

        self.structures = []
        self.objectives = []

    def draw(self):
        for tile in self.tiles.values():
            tile.draw()

    # These event methods are called the Game Manage (brock_purdy.py)
    def animate_turn(self):
        pass

    def end_of_turn(self):
        pass


    



        


