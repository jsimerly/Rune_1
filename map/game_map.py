from .game_tile import GameTile
from .loadouts.map_layout import MapLayout
from typing import List
import pygame as pg

from hex import Point

class GameMap:
    def __init__(self, map: MapLayout, screen):
        self.tiles = map.generate_map(screen, self)
        self.screen = screen
        self.layout = map.layout

        self.structures = []
        self.objectives = []

    def draw(self):
        for tile in self.tiles.values():
            tile.draw()

    def draw_movement_path(self, path: List[GameTile]):
        center_pixels = []
        for tile in path:
            pixel_coord = self.layout.hex_to_pixel(tile)
            center_pixels.append(pixel_coord)

        if len(center_pixels) > 0:
            surface = pg.Surface(self.screen.get_size(), pg.SRCALPHA)
            color = (221, 227, 220, 150)
            pg.draw.lines(surface, color, False, center_pixels, 3)
            self.screen.blit(surface, (0,0))


    def redraw_tiles(self, tiles:List[GameTile]):
        for tile in tiles:
            tile.redraw_neighbors()

    def redraw_tile_borders(self, tiles:List[GameTile]):
        for tile in tiles:
            tile.reset_border()

    # These event methods are called the Game Manage (brock_purdy.py)
    def animate_turn(self):
        pass

    def end_of_turn(self):
        pass


    



        


