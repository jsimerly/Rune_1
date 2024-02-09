from __future__ import annotations
from in_game.event_bus import EventBus
from in_game.ecs.systems.system_base import System
from in_game.ecs.components.vision_component import VisionComponent
from in_game.ecs.components.occupier_component import OccupierComponent
from in_game.ecs.components.fog_of_war import FogOfWarComponent
from in_game.ecs.components.map_interaction_component import TileMapInteractionComponent
from algorithms import hex_radius
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from map.tile import GameTile


class VisionSystem(System):
    required_components = [VisionComponent, OccupierComponent]

    def __init__(self, event_bus: EventBus) -> None:
        super().__init__(event_bus)
        

    def update_vision(self):
        for entity in self.entities:
            vision_comp: VisionComponent = entity.get_component(VisionComponent)
            occupier_comp: OccupierComponent = entity.get_component(OccupierComponent)

            if vision_comp.is_blind:
                continue
            
            tiles_in_vision: set[GameTile] = set()
            for entity_tile in occupier_comp.tiles:
                tiles_in_radius = hex_radius(entity_tile, vision_comp.vision_radius) 
                for potential_tile in tiles_in_radius:
                    if self.is_tile_in_los(entity_tile, potential_tile):
                        tiles_in_vision.add(potential_tile)

            for vision_tile in tiles_in_vision:
                fog_of_war_comp: FogOfWarComponent = vision_tile.get_component(FogOfWarComponent)
                fog_of_war_comp.is_fog_of_war = False


    def is_tile_in_los(self, center_tile: GameTile, target_tile:GameTile):
        tiles_in_los = center_tile.line_to(target_tile)
        for tile in tiles_in_los:
            map_interaction_comp: TileMapInteractionComponent = tile.get_component(TileMapInteractionComponent)
            if map_interaction_comp.blocks_los:
                return False
        return True
 

        

                
