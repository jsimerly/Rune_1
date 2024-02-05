from __future__ import annotations
from in_game.event_bus import EventBus
from in_game.ecs.systems.system_base import System
from in_game.action_state import ActionStateManager
from in_game.ecs.components.occupancy_component import OccupancyComponent
from in_game.entities.buildings.building_base import Building
from in_game.entities.objectives.objective_base import Objective
from in_game.entities.characters.character_base import Character
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from map.tile import GameTile

class ClickSystem(System):
    def __init__(self, event_bus: EventBus, action_state: ActionStateManager) -> None:
        super().__init__(event_bus)
        self.action_state = action_state
        self.event_bus = event_bus
        self.event_bus.subscribe('tile_clicked', self.handle_tile_clicked)
        self.event_bus.subscribe('tile_drag_started', self.handle_tile_drag_start)
        self.event_bus.subscribe('tile_dragging', self.handle_tile_dragging)
        self.event_bus.subscribe('tile_drag_ended', self.handle_tile_drag_ended)


    def handle_tile_clicked(self, tile: GameTile):
        occupancy_component: OccupancyComponent = tile.get_component(OccupancyComponent)

        for occupant in occupancy_component.occupants:
            if isinstance(occupant, Character):
                self.event_bus.publish('character_selected', occupant)
            if isinstance(occupant, Building):
                self.event_bus.publish('building_selected', occupant)
                print('building selected')
            if isinstance(occupant, Objective):
                self.event_bus.publish('objective_selected', occupant)
            

        # self.action_state.movement() 
        # start handling click whats happening based on where they're clcking and what they're clicking
        ...

    def handle_tile_drag_start(self, tile):
        ...

    def handle_tile_dragging(self, tile):
        ...

    def handle_tile_drag_ended(self, tile):
        ...