from __future__ import annotations
from in_game.event_bus import EventBus

from in_game.ecs.entity import Entity
from .system_base import System
from in_game.ecs.components.occupancy_component import OccupancyComponent
from in_game.ecs.components.occupier_component import OccupierComponent
from in_game.ecs.components.sprite_component import SpriteComponent

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from entity import Entity
    from map.tile import GameTile

class OccupancySystem(System):
    required_components = [OccupancyComponent]
    def __init__(self, event_bus: EventBus) -> None:
        super().__init__(event_bus)
        self.event_bus.subscribe('spawn_to_tile', self.spawn_to_tile)
        self.event_bus.subscribe('entity_moved_to_tile', self.move_entity_to_tile)
        self.event_bus.subscribe('entity_dragged_to_tile', self.move_entity_to_tile)

    def spawn_to_tile(self, tile: GameTile, entity: Entity):
        occupier_comp: OccupierComponent = entity.get_component(OccupierComponent)
        for remove_tile in occupier_comp.tiles:
            occupancy_comp: OccupancyComponent = remove_tile.get_component(OccupancyComponent)
            occupancy_comp.occupants.remove(entity)

        occupier_comp.tiles = set()
        self.add_occupant(tile, entity)

    def move_entity_to_tile(self, entity: Entity, from_tile: GameTile, to_tile: GameTile):
         self.remove_occupant(entity, from_tile)
         self.add_occupant(to_tile, entity)

    def add_occupant(self, entity_to_be_occupied: Entity, occupant: Entity):
        if occupant.has_component(OccupierComponent):
            occupancy_component: OccupancyComponent = entity_to_be_occupied.get_component(OccupancyComponent)
            occupier_component: OccupierComponent = occupant.get_component(OccupierComponent)

            occupier_component.tiles.add(entity_to_be_occupied)
            occupancy_component.occupants.add(occupant)
            print(occupier_component.tiles)

    def remove_occupants(self, entity_to_remove: Entity, occupants: list[Entity] | set[Entity]):
        for occupant in occupants:
            occupancy_comp: OccupancyComponent = occupant.get_component(OccupancyComponent)
            if occupancy_comp:
                occupancy_comp.occupants.remove(entity_to_remove)

            occupier_component: OccupierComponent = entity_to_remove.get_component(OccupierComponent)

            occupier_component.tiles.remove(occupant)

    def remove_occupant(self, entity_to_remove: Entity, occupant: Entity):
            occupancy_component: OccupancyComponent = occupant.get_component(OccupancyComponent)
            occupier_component: OccupierComponent = entity_to_remove.get_component(OccupierComponent)

            occupier_component.tiles.remove(occupant)
            occupancy_component.occupants.remove(entity_to_remove)
    

              

