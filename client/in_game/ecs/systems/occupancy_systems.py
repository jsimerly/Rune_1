from __future__ import annotations

from in_game.ecs.entity import Entity
from .system_base import System
from in_game.ecs.components.occupancy_component import OccupancyComponent
from in_game.ecs.components.occupier_component import OccupierComponent
from in_game.ecs.components.sprite_component import SpriteComponent

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from entity import Entity

class OccupancySystem(System):
    required_components = [OccupancyComponent]

    def add_occupant(self, entity_to_be_occupied: Entity, occupant: Entity):
        if occupant.has_component(OccupierComponent):
            occupancy_component: OccupancyComponent = entity_to_be_occupied.get_component(OccupancyComponent)
            occupier_component: OccupierComponent = occupant.get_component(OccupierComponent)

            occupier_component.tiles.add(entity_to_be_occupied)
            occupancy_component.occupants.add(occupant)

    def remove_occupant(self, entity_to_remove: Entity, occupant: Entity):
            occupancy_component: OccupancyComponent = entity_to_remove.get_component(OccupancyComponent)
            occupier_component: OccupierComponent = occupant.get_component(OccupierComponent)

            occupier_component.tiles.remove(entity_to_remove)
            occupancy_component.occupants.remove(occupant)

              

