
from __future__ import annotations
from components.abstact_component import AbstactComponent
from algorithms import hex_radius

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from map.game_tile import GameTile

class VisionComponent(AbstactComponent):
    def __init__(self, entity_tile: GameTile, vision_range:int) -> None:
        self.tile = entity_tile
        self.range = vision_range
    
    def get_tiles_in_los(self):
        tiles_in_range = hex_radius(self.tile, radius=self.range)

        visible_tiles = [] 
        for tile_in_range in tiles_in_range:
            tiles_in_the_way = self.tile.get_tiles_in_line(tile_in_range)
            vision_blocked = False
            
            for tile_in_the_way in tiles_in_the_way:
                if tile_in_the_way.map_interaction.blocks_vision:
                    vision_blocked = True
                    break  
            
            if not vision_blocked:
                visible_tiles.append(tile_in_range)

        return visible_tiles


            
            