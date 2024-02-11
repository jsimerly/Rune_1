from __future__ import annotations
from in_game.event_bus import EventBus

from in_game.ecs.entity import Entity
from .system_base import System
from in_game.ecs.components.occupancy_component import OccupancyComponent
from in_game.ecs.components.occupier_component import OccupierComponent
from in_game.ecs.components.sprite_component import SpriteComponent
from in_game.ecs.components.map_interaction_component import MapInteractionComponent, TileMapInteractionComponent

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
        self.event_bus.subscribe('remove_entity_from_tile', self.remove_occupant)

    def spawn_to_tile(self, tile: GameTile, entity: Entity):
        occupier_comp: OccupierComponent = entity.get_component(OccupierComponent)
        for remove_tile in occupier_comp.tiles:
            occupancy_comp: OccupancyComponent = remove_tile.get_component(OccupancyComponent)
            occupancy_comp.occupants.remove(entity)

        occupier_comp.tiles = set()
        self.add_occupant(tile, entity)

    def move_entity_to_tile(self, entity: Entity, from_tile: GameTile, to_tile: GameTile):
         if from_tile:
            self.remove_occupant(entity, from_tile)
         self.add_occupant(to_tile, entity)

    def add_occupant(self, entity_to_be_occupied: Entity, occupant: Entity):
        if occupant.has_component(OccupierComponent):
            occupancy_component: OccupancyComponent = entity_to_be_occupied.get_component(OccupancyComponent)
            occupier_component: OccupierComponent = occupant.get_component(OccupierComponent)

            occupier_component.tiles.add(entity_to_be_occupied)
            occupancy_component.occupants.add(occupant)
            self.handle_add_map_interaction(entity_to_be_occupied)

    def remove_occupants(self, entity_to_remove: Entity, occupants: list[Entity] | set[Entity]):
        for occupant in occupants:
            occupancy_comp: OccupancyComponent = occupant.get_component(OccupancyComponent)
            if occupancy_comp:
                occupancy_comp.occupants.remove(entity_to_remove)
                
            occupier_component: OccupierComponent = entity_to_remove.get_component(OccupierComponent)

            occupier_component.tiles.remove(occupant)
            self.handle_add_map_interaction(occupant)

    def remove_occupant(self, entity: Entity, tile: Entity):
        occupancy_component: OccupancyComponent = tile.get_component(OccupancyComponent)
        occupier_component: OccupierComponent = entity.get_component(OccupierComponent)
        if tile in occupier_component.tiles:
            occupier_component.tiles.remove(tile)
        if entity in occupancy_component.occupants:
            occupancy_component.occupants.remove(entity)
        self.handle_add_map_interaction(tile)

    def handle_add_map_interaction(self, tile: Entity):
        ''' Priority 
            is_passable: False
            blocks_los: True
            can_end_on: False
            can_pierce: False
            hides_occupants: True
            is_slowing: True
        '''
        occupancy_comp: OccupancyComponent = tile.get_component(OccupancyComponent)
        tile_map_int_comp: TileMapInteractionComponent = tile.get_component(TileMapInteractionComponent)

        # Initialize properties with their defaults
        blocks_los = tile_map_int_comp.default_blocks_los
        is_passable = tile_map_int_comp.default_is_passable
        can_end_on = tile_map_int_comp.default_can_end_on
        can_pierce = tile_map_int_comp.default_can_pierce
        hides_occupants = tile_map_int_comp.default_hides_occupants
        is_slowing = tile_map_int_comp.default_is_slowing

        # Loop through each occupant to check for priority properties
        for occupier in occupancy_comp.occupants:
            entity_map_inter_comp: MapInteractionComponent = occupier.get_component(MapInteractionComponent)
            if entity_map_inter_comp:

                # Update properties based on occupant's priority
                blocks_los = blocks_los or entity_map_inter_comp.blocks_los
                is_passable = is_passable and entity_map_inter_comp.is_passable
                can_end_on = can_end_on and entity_map_inter_comp.can_end_on
                can_pierce = can_pierce and entity_map_inter_comp.can_pierce
                hides_occupants = hides_occupants or entity_map_inter_comp.hides_occupants
                is_slowing = is_slowing or entity_map_inter_comp.is_slowing

        # Apply the updated values to the tile's interaction component
        tile_map_int_comp.blocks_los = blocks_los
        tile_map_int_comp.is_passable = is_passable
        tile_map_int_comp.can_end_on = can_end_on
        tile_map_int_comp.can_pierce = can_pierce
        tile_map_int_comp.hides_occupants = hides_occupants
        tile_map_int_comp.is_slowing = is_slowing


    






    

              

