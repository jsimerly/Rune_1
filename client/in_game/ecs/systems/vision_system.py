from __future__ import annotations
from in_game.event_bus import EventBus
from in_game.ecs.systems.system_base import System
from in_game.ecs.components.vision_component import VisionComponent
from in_game.ecs.components.occupier_component import OccupierComponent
from in_game.ecs.components.fog_of_war import FogOfWarComponent
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
            for tile in occupier_comp.tiles:
                tiles_in_view = hex_radius(tile, vision_comp.vision_radius) #update this algo to include vision
                tiles_in_vision.update(tiles_in_view)

            for tile in tiles_in_vision:
                fog_of_war_comp: FogOfWarComponent = tile.get_component(FogOfWarComponent)
                fog_of_war_comp.is_fog_of_war = False
                
