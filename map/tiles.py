from typing import Optional
from .game_tile import GameTile


class Grass(GameTile):
    def __init__(self, q: int, r: int, layout, screen, has_coords):
        super().__init__(
            q=q, r=r, layout=layout, screen=screen,
            has_coords=has_coords,
            surface_color=(140, 181, 101), 
        )

class Tree(GameTile):
    def __init__(self, q: int, r: int, layout, screen, has_coords):
        super().__init__(
            q, r, layout, screen,
            has_coords=has_coords,
            surface_color=(12, 36, 2), 
        )

#Different from trees only because some characters interact directly with trees.
class Rock(GameTile):
    def __init__(self, q: int, r: int, layout, screen, has_coords):
        super().__init__(
            q, r, layout, screen,
            has_coords=has_coords,
            surface_color=(58,50,50), 

        )

class Water(GameTile):
    def __init__(self, q: int, r: int, layout, screen, has_coords):
        super().__init__(
            q, r, layout, screen,
            has_coords=has_coords, 
            surface_color=(152, 216, 227), 
        )

class Brush(GameTile):
    def __init__(self, q: int, r: int, layout, screen, has_coords):
        super().__init__(
            q, r, layout, screen,
            has_coords=has_coords,
            surface_color=(191, 174, 46), 
        )

class RoughTerrian(GameTile):
    def __init__(self, q: int, r: int, layout, screen, has_coords):
        super().__init__(
            q, r, layout, screen,
            has_coords=has_coords,
            surface_color=(94, 122, 66), 
        )

    