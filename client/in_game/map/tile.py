from __future__ import annotations
from typing import List, TYPE_CHECKING, Tuple, Optional
from in_game.ecs.components.component_base import Component
from in_game.ecs.entity import Entity
from in_game.ecs.components.sprite_component import TileSpriteComponent
from in_game.ecs.components.visual_edge_component import VisualHexEdgeComponent, SelectedHexEdgeComponent
from in_game.ecs.components.screen_position_component import ScreenPositionComponent
from in_game.ecs.components.occupancy_component import OccupancyComponent
from in_game.ecs.components.fog_of_war import FogOfWarComponent

if TYPE_CHECKING:
    from map.map import GameMap

class GameTile(Entity):
    direction_vectors = [
        (-1, 0, 1), (0, -1, 1), (1, -1, 0),
        (1, 0, -1), (0, 1, -1), (-1, 1, 0)
    ]

    def __init__(
            self,  q: int, r: int, map: GameMap, entity_id:str,
            sprite_image,
            surface_color, is_passable, can_pierce, can_end_on, blocks_vision, hides_occupants, is_slowing,
        ) -> None:       
        self.q, self.r = q, r
        self.s = -q - r
        self.map: GameMap = map

        position_component = ScreenPositionComponent((self.map.tile_center_to_pixel(self)))
        tile_sprite_component = TileSpriteComponent(
            sprite_image, surface_color, self.verticies, self.map.tile_size,
            self.map.tile_center_to_pixel(self)
        )
        visual_edge_component = VisualHexEdgeComponent(
            self.verticies, transparent=True
        )
        selected_edge_component = SelectedHexEdgeComponent(
            self.verticies
        )
        occupancy_component = OccupancyComponent(set())
        fog_of_war_component = FogOfWarComponent()
        components = [
            position_component, 
            tile_sprite_component, 
            visual_edge_component,
            selected_edge_component,
            occupancy_component,
            fog_of_war_component,
        ]
        super().__init__(entity_id, components)


    '''
        Hex traits
    '''
    def set_game_map(self, map: GameMap):
        self.map = map

    def __eq__(self, other) -> bool:
        if isinstance(other, GameTile):
            return self.q == other.q and self.r == other.r
        return False
    
    def __ne__(self, other) -> bool:
        return not self.__eq__(other)
    
    def __add__(self, other) -> Optional[GameTile]:
        if isinstance(other, GameTile):
            new_tile_coords = (self.q + other.q, self.r + other.r, self.s + other.s)
            return self.get_map_tile(new_tile_coords)
        
        return NotImplemented
    
    def __sub__(self, other) -> Optional[GameTile]:
        if isinstance(other, GameTile):
            new_tile_cords = (self.q - other.q, self.r - other.r, self.s - other.s)
            return self.get_map_tile(new_tile_cords)    
    
        return NotImplemented
    
    def __mul__(self, other) -> Optional[GameTile]:
        if isinstance(other, GameTile):
            new_tile_coords = (self.q * other.q, self.r * other.r, self.s * other.s)
            return self.get_map_tile(new_tile_coords)
        
    def get_map_tile(self, coords: Tuple[int, int]) -> Optional[GameTile]:
        return self.map.get_tile(coords)

    def __hash__(self) -> Tuple[int, int]:
        return hash(self.axial)
    
    @property
    def axial(self):
        return (self.q, self.r)
    
    @property
    def center_pixel(self) -> tuple(int,int):
        return self.map.tile_center_to_pixel(self)

    @property
    def verticies(self) -> List[Tuple[int,int]]:
        return self.map.get_tile_verticies(self.center_pixel)
    
    def magnitude(self, hex: GameTile) -> int:
        ''' We divide by two because we're using a 3D grid system with a plane through it at x + y + z = 0.
        Typically, in a 3D system, we would calculate the length of this vector using the distance from 0, 0, 0.
        But, because we're only using diagnols, as opposed to every block in a discrete 3D grid, that means we're
        double counting using Manhattan distances. '''

        return int((abs(hex[0]) + abs(hex[1]) + abs(hex[2]))/2)
    
    def distance_to(self, other: GameTile) -> int:
        vector = (self.q - other.q, self.r - other.r, self.s - other.s)
        return self.magnitude(vector)
    
    def direction(self, direction: int) -> (int, int, int):
        if -6 <= direction <= 5:
            return self.direction_vectors[direction]
        raise ValueError('direction must be between -5 to 5')
    
    def neighbor(self, direction) -> Optional[GameTile]:
        new_tile = self + self.direction(direction)
        return new_tile # will return None if not on map

    def get_all_neighbors(self) -> List[GameTile]:
        neighbors = []
        for i in range(6):
            neighbor = self.neighbor(i)
            if neighbor:
                neighbors.append(neighbor)
        return neighbors
    
    #linear interpolation
    def lerp(self, a: int, b:int, t: float) -> int:
        return a * (1-t) + (b*t)

    def tile_lerp(self, target_tile: GameTile, t) -> Optional[GameTile]:
        '''returns the tile closest to the t value in the line from self to the target tile'''
        fractional_hex_coord = (
            self.lerp(self.q, target_tile.q, t),
            self.lerp(self.r, target_tile.r, t),
            self.lerp(self.s, target_tile.s, t)
        )
        return self.fractional_to_tile(fractional_hex_coord)

    def fractional_to_tile(self, q, r, s) -> Optional[GameTile]:
        q = int(round(q))
        r = int(round(r))
        s = int(round(s))

        dq = abs(q-q)
        dr = abs(r-r)
        ds = abs(s-s)

        if (dq > dr and dq > ds):
            q = -r -s        
        elif (dr > ds):
            r = -q -s
        else:
            s = -q -r
        return self.get_map_tile(q, r)
    
    def line_to(self, target_tile: GameTile) -> List[GameTile]:
        N = self.distance_to(target_tile)
        tiles = []
        for i in range(N):
            tile = self.tile_lerp(target_tile, 1./N * i)
            if tile:
                tiles.append(tile)
        return tiles
    
   

    

