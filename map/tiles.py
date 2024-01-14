from typing import Optional
from .game_tile import GameTile


class Grass(GameTile):
    def __init__(self, q: int, r: int, layout):
        super().__init__(
            q=q, r=r, layout=layout,
            
            surface_color=(140, 181, 101), 
            is_passable=True, 
            can_pierce=True,
            can_end_on=True, 
            blocks_vision=False, 
            hides_occupants=False, 
            is_slowing=False, 
        )

    def __repr__(self) -> str:
        return super().__repr__()

class Tree(GameTile):
    def __init__(self, q: int, r: int, layout):
        super().__init__(
            q, r, layout,
            
            surface_color=(12, 36, 2), 
            is_passable=False, 
            can_pierce=False,
            can_end_on=False, 
            blocks_vision=True, 
            hides_occupants=True, 
            is_slowing=False, 
        )

#Different from trees only because some characters interact directly with trees.
class Rock(GameTile):
    def __init__(self, q: int, r: int, layout):
        super().__init__(
            q, r, layout,
            
            surface_color=(58,50,50), 
            is_passable=False, 
            can_pierce=False,
            can_end_on=False, 
            blocks_vision=False, 
            hides_occupants=False, 
            is_slowing=False, 
        )

class Water(GameTile):
    def __init__(self, q: int, r: int, layout):
        super().__init__(
            q, r, layout,
             
            surface_color=(152, 216, 227), 
            is_passable=False, 
            can_pierce=True,
            can_end_on=False, 
            blocks_vision=False, 
            hides_occupants=False, 
            is_slowing=False, 
        )

class Brush(GameTile):
    def __init__(self, q: int, r: int, layout):
        super().__init__(
            q, r, layout,
            
            surface_color=(191, 174, 46), 
            is_passable=True, 
            can_pierce=True,
            can_end_on=True, 
            blocks_vision=True, 
            hides_occupants=True, 
            is_slowing=False, 
        )

class RoughTerrian(GameTile):
    def __init__(self, q: int, r: int, layout):
        super().__init__(
            q, r, layout,
            
            surface_color=(94, 122, 66),
            is_passable=True, 
            can_pierce=True,
            can_end_on=True, 
            blocks_vision=False, 
            hides_occupants=False, 
            is_slowing=True,
        )

    