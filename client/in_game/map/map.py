from __future__ import annotations
from typing import List, Dict, Callable, TYPE_CHECKING, Optional, Tuple
import pygame as pg
from settings import SCREEN_HEIGHT
from math import radians, cos, sin
from .tile_factory import TileFactory
from mouse_inputs import Click, DragStart, Dragging, DragEnd, MouseInput

if TYPE_CHECKING:
    from map.loadouts.loadout_base import MapLoadout
    from character.abs_character import AbstractCharacter
    from map.tile import GameTile
    from team.team import Team
    from building.abs_building import AbstractBuilding
    from event_bus import EventBus
    from mouse_inputs import MouseInput


class GameMap:
    tile_size = (40, 40) # adjust this based on settintgs
    origin = (1000, SCREEN_HEIGHT//2)
    skew = 0

    def __init__(self, map_loadout: MapLoadout, event_bus: EventBus) -> None:
        self.event_bus = event_bus
        self.orientation = map_loadout.orientation
        self.tiles: Dict[Tuple[int,int], GameTile] = dict()

    def get_tile(self, coord: Tuple[int, int]):
        return self.tiles.get(coord)
    
    ''' Game Tile Management '''
   
    def tile_center_to_pixel(self, tile: GameTile) -> Tuple[int ,int]:
        M = self.orientation
        x = (M.f0 * tile.q + M.f1 * tile.r) * self.tile_size[0]
        y = (M.f2 * tile.q + M.f3 * tile.r) * self.tile_size[1]
        coords = (x + self.origin[0], y + self.origin[1])
        return coords
    
    def pixel_to_tile(self, pixel: Tuple[int ,int]) -> Optional[GameTile]:
        M = self.orientation
        x, y = pixel
        pt_x = (x - self.origin[0]) / self.tile_size[0]
        pt_y = (y - self.origin[1]) / self.tile_size[1]

        q1 = M.b0 * pt_x + M.b1 * pt_y
        r1 = M.b2 * pt_x + M.b3 * pt_y
        s1 = -q1 - r1
        int_coords = self.fractional_to_int(q1, r1, s1)
        tile_cords = (int_coords[0], int_coords[1])
        return self.get_tile(tile_cords)


    def fractional_to_int(self, q1: float, r1: float, s1: float) -> Tuple[int, int, int]:
        q = int(round(q1))
        r = int(round(r1))
        s = int(round(s1))

        dq = abs(q1-q)
        dr = abs(r1-r)
        ds = abs(s1-s)

        if (dq > dr and dq > ds):
            q = -r -s        
        elif (dr > ds):
            r = -q -s
        else:
            s = -q -r

        return (q, r, s)
    
    def get_corner_offset(self, corner: int) -> Tuple[int, int]:
        angle_deg = 60 * corner + self.orientation.start_angle
        angle_rad = radians(angle_deg)
        x = self.tile_size[0] * cos(angle_rad)
        y = self.tile_size[1] * sin(angle_rad)

        x += self.skew * y
        return (x, y)

    def get_tile_verticies(self, p: Tuple[int, int]) -> List[(int, int)]:
        ''' get the verticies for a tile based on the center point, orienation and size of the hex'''
        verticies = []
        for corner in range(6):
            offset = self.get_corner_offset(corner)
            x, y = (p[0] + offset[0], p[1] + offset[1])
            x = int(round(x, 0))
            y = int(round(y, 0))
            verticies.append((x, y))
        return verticies
    

    


    

    
            


