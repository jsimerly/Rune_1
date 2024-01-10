from .game_tile import GameTile
from .loadouts.map_layout import MapLayout
from typing import List, Set, Tuple
import pygame as pg
from utils import time_it

from hex import Point

class GameMap:
    def __init__(self, map: MapLayout, screen):
        self.tiles = map.generate_map(screen, self)
        self.screen = screen
        self.layout = map.layout

        self.render = RerenderComponent(self)
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


class RerenderComponent:
    def __init__(self, game_map:GameMap):
        self.game_map: GameMap = game_map
        self.full_tiles: Set[GameTile] = set()
        self.borders: Set[GameTile] = set()
        self.selection: Set[GameTile] = set()
        self.movement: List[Tuple[List[GameTile], (int,int,int)]] = []
        self.abilities:  List[GameTile] = []

    def run_all(self):
        self.render_full_tiles()
        self.render_borders()
        self.render_selection()
        self.render_movement()
        self.render_abliities()
        self.reset()

    def reset(self):
        self.full_tiles = set()
        self.borders = set()
        self.selection = set()
        self.movement = []
        self.abilities = []

    def render_full_tiles(self):
        for tile in self.full_tiles:
            self.tile_full_draw(tile)

    def tile_full_draw(self, tile:GameTile):
        tile.draw()

    def render_borders(self):
        for tile in self.borders:
            tile.draw_border()
    
    def render_selection(self):
        for tile in self.selection:
            tile.draw_border()

    def render_movement(self):
        for move_queue in self.movement:
            self.draw_movement_path(move_queue[0], move_queue[1])

    def draw_movement_path(self, path: List[GameTile], color:(int,int,int)):
        center_pixels = []
        for tile in path:
            pixel_coord = self.game_map.layout.hex_to_pixel(tile)
            center_pixels.append(pixel_coord)

        if len(center_pixels) > 0:
            surface = pg.Surface(self.game_map.screen.get_size(), pg.SRCALPHA)
            color = (color[0], color[1], color[2], 50)
            pg.draw.lines(surface, color, False, center_pixels, 3)
            self.game_map.screen.blit(surface, (0,0))
            

    def render_abliities(self):
        pass
            
    def add_full_tiles(self, game_tiles: List[GameTile]):
        if game_tiles:
            self.full_tiles.update(game_tiles)

    def remove_full_tile(self, game_tile: GameTile):
        self.full_tiles.discard(game_tile)

    def add_selection(self, game_tile: List[GameTile]):
        if game_tile:
            self.selection.add(game_tile)

    def remove_selection(self, game_tile: GameTile):
        self.selection.discard(game_tile)

    def add_borders(self, game_tiles: List[GameTile]):
        if game_tiles:
            self.borders.update(game_tiles)

    def remove_border(self, game_tile: GameTile):
        self.borders.discard(game_tile)

    def add_movement(self, game_tiles: List[GameTile], color:(int,int)=(200, 0, 200)):
        if game_tiles and color:
            self.add_full_tiles(game_tiles) #to prevent repeat transparent color.
            self.movement.append((game_tiles, color))

    def remove_movement(self, game_tiles: List[GameTile]):
        for i, movement_tuple in enumerate(self.movement):
            movement_queue = movement_tuple[0]
            if game_tiles[0] == movement_queue[0] and game_tiles[-1] == movement_queue[-1]:
                self.movement.pop(i)

    def add_ability(self):
        print('need to implement: add ability')

    def remove_ability(self):
        print('need to implmenet: remove ability')



        


