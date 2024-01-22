from __future__ import annotations
from .abstact_component import AbstactComponent
from typing import TYPE_CHECKING, Any, List, Set, Optional, Dict, Tuple
from client.utils import time_it
from client.in_game.surfaces import GameSurfaces
import pygame as pg
from client.algorithms import astar, hex_reachable

if TYPE_CHECKING:
    from character.abs_character import AbstractCharacter
    from map.game_tile import GameTile

    
class MovementQueue:
    def __init__(self, color: Tuple[int,int,int]):
        self.queue: Optional[List[GameTile]] = []
        self.pixels: List[Tuple[int,int]] = []
        self.game_surfaces = GameSurfaces()
        self.color = color + (150,)

    def __call__(self) -> Optional[List[GameTile]]:
        return self.queue

    @property
    def is_empty(self) -> bool:
        return len(self.queue) == 0

    @property
    def start_tile(self) -> GameTile:
        if not self.is_empty:
            return self.queue[0]
        
    @property
    def end_tile(self) -> GameTile:
        if not self.is_empty:
            return self.queue[-1]
        
    def add_tile(self, tile:GameTile):
        self.queue.append(tile)
        self.handle_update()

    def remove_tile(self, tile:GameTile):
        self.queue.remove(tile)
        self.handle_update()

    def remove_end_tile(self):
        self.queue.pop()
        self.handle_update()

        
    def set_queue(self, tiles: List[GameTile]):
        self.queue = tiles
        self.handle_update()

    def set_queue_to(self, start_tile: GameTile, end_tile: GameTile) -> bool:
        self.queue = astar(start_tile, end_tile)
        self.handle_update()

    def clear(self):
        self.queue = []
        self.handle_update()


    ''' Draw '''
    def draw(self, screen: pg.Surface):
        if len(self.pixels) >= 2:
            trans_surface = pg.Surface(screen.get_size(), pg.SRCALPHA)
            pg.draw.lines(trans_surface, self.color, False, self.pixels, 5)
            screen.blit(trans_surface, (0, 0))

    def handle_update(self):
        if len(self.queue) >= 2:
            self.pixels = [tile.center_pixel for tile in self.queue]
            self.game_surfaces.add_to_layer(self.game_surfaces.movement, self)
        else:
            self.game_surfaces.remove_from_layer(self.game_surfaces.movement, self)


class MovementComponent(AbstactComponent):
    def __init__(self, color: Tuple[int,int,int]) -> None:
        super().__init__()
        self.range = 5
        self.queue: MovementQueue = MovementQueue(color)

    ''' Movement '''
    def move(self, start_tile: GameTile, end_tile:GameTile) -> List[GameTile]:
        self.queue.set_queue_to(start_tile, end_tile)
        return self.queue()
    
    def drag_move_new_tile(self, tile:GameTile):
        if len(self.queue()) >= 2:
            if tile == self.queue()[-2]:
                self.queue.remove_end_tile()

        if tile != self.queue.end_tile:
            self.queue.add_tile(tile)
    
    def clear_move(self) -> Tuple[GameTile, GameTile]:
        start_tile = self.queue.start_tile
        end_tile = self.queue.end_tile
        self.queue.clear()    
        return start_tile, end_tile

    def find_possible_tiles(self, from_tile: GameTile) -> List[GameTile]:
        possible = hex_reachable(from_tile, self.range)
        return possible

           



                



        


    
        