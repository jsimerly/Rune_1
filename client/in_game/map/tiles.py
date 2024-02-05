from __future__ import annotations
from typing import Optional, TYPE_CHECKING
from .tile import GameTile
import pygame as pg

if TYPE_CHECKING:
    from map.map import GameMap


grass_image = pg.image.load('in_game/map/images/grass.png')
class Grass(GameTile):
    def __init__(self, q: int, r: int, map: GameMap, entity_id: str):
        super().__init__(
            q=q, r=r, map=map,entity_id=entity_id,
            sprite_image=grass_image,
            surface_color=(181, 194, 132), 
            is_passable=True, 
            can_pierce=True,
            can_end_on=True, 
            blocks_vision=False, 
            hides_occupants=False, 
            is_slowing=False, 
        )

    def __repr__(self) -> str:
        return super().__repr__()

tree_image = pg.image.load('in_game/map/images/tree.webp')
class Tree(GameTile):
    def __init__(self, q: int, r: int, map: GameMap, entity_id:str):
        super().__init__(
            q, r, map=map, entity_id=entity_id,
            sprite_image=tree_image,
            surface_color=(55, 117, 59), 
            is_passable=False, 
            can_pierce=False,
            can_end_on=False, 
            blocks_vision=True, 
            hides_occupants=True, 
            is_slowing=False, 
        )

#Different from trees only because some characters interact directly with trees.
class Rock(GameTile):
    def __init__(self, q: int, r: int, map: GameMap, entity_id:str):
        super().__init__(
            q, r, map, entity_id=entity_id,
            sprite_image=grass_image,            
            surface_color=(58,50,50), 
            is_passable=False, 
            can_pierce=False,
            can_end_on=False, 
            blocks_vision=False, 
            hides_occupants=False, 
            is_slowing=False, 
        )

class Water(GameTile):
    def __init__(self, q: int, r: int, map: GameMap, entity_id:str):
        super().__init__(
            q, r, map, entity_id=entity_id,
            sprite_image=grass_image,            
            surface_color=(152, 216, 227), 
            is_passable=False, 
            can_pierce=True,
            can_end_on=False, 
            blocks_vision=False, 
            hides_occupants=False, 
            is_slowing=False, 
        )

brush_image = pg.image.load('in_game/map/images/brush.webp')
class Brush(GameTile):
    def __init__(self, q: int, r: int, map: GameMap, entity_id:str):
        super().__init__(
            q, r, map, entity_id=entity_id,
            sprite_image=brush_image,            
            surface_color=(160, 194, 81), 
            is_passable=True, 
            can_pierce=True,
            can_end_on=True, 
            blocks_vision=True, 
            hides_occupants=True, 
            is_slowing=False, 
        )

class RoughTerrian(GameTile):
    def __init__(self, q: int, r: int, map: GameMap, entity_id:str):
        super().__init__(
            q, r, map, entity_id=entity_id,
            sprite_image=grass_image,            
            surface_color=(94, 122, 66),
            is_passable=True, 
            can_pierce=True,
            can_end_on=True, 
            blocks_vision=False, 
            hides_occupants=False, 
            is_slowing=True,
        )

    