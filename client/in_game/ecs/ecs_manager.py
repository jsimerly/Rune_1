from __future__ import annotations
from .systems.render_systems import DrawSpriteSystem, DrawTileSystem, DrawHexEdgeSystem, DrawSelectedHexSystem, DrawFogOfWarSystem, DrawAuraSystem, DrawMovementSystem
from .systems.ui_system import UISystem
from .systems.movement_system import MovementSystem
from .systems.render_systems import RenderSystem
from .systems.occupancy_systems import OccupancySystem
from .systems.team_system import TeamSystem
from .systems.click_systems import ClickSystem
from .systems.spawning_system import SpawningSystem
from .systems.vision_system import VisionSystem
from typing import TYPE_CHECKING, List
import pygame as pg

if TYPE_CHECKING:
    from map.map import GameMap
    from action_state import ActionStateManager
    from in_game.event_bus import EventBus
    from in_game.ecs.entity import Entity

class ECSManager:
    def __init__(self, event_bus: EventBus, action_state: ActionStateManager, game_map: GameMap) -> None:
        self.all_entities: dict[str, Entity] = {}
        self.game_map = game_map
        self.event_bus = event_bus
        self.action_state = action_state
        self.click_system = ClickSystem(event_bus=event_bus, action_state=action_state, game_map=self.game_map)

        ''' Rendering Systems'''
        self.tile_sprite_system = DrawTileSystem(event_bus=event_bus)
        self.border_system = DrawHexEdgeSystem(event_bus=event_bus)
        self.selected_system = DrawSelectedHexSystem(event_bus=event_bus, action_state=action_state)
        self.draw_aura_system = DrawAuraSystem(event_bus=event_bus)
        self.building_sprite_system = DrawSpriteSystem(event_bus=event_bus)
        self.objective_sprite_system = DrawSpriteSystem(event_bus=event_bus)
        self.draw_movement_system = DrawMovementSystem(event_bus=event_bus)
        self.character_sprite_system = DrawSpriteSystem(event_bus=event_bus)
        self.draw_fog_of_war_system = DrawFogOfWarSystem(event_bus=event_bus)
        #ability system
        self.ui_system = UISystem(event_bus=event_bus)

        self.render_systems: List[RenderSystem] = [
            self.tile_sprite_system,
            self.draw_aura_system,
            self.border_system,
            self.selected_system,
            
            self.building_sprite_system,
            self.objective_sprite_system,
            self.draw_fog_of_war_system,
            self.draw_movement_system,
            self.character_sprite_system,
            
            self.ui_system,
        ]

        ''''''
        self.occupancy_system = OccupancySystem(event_bus=event_bus)
        self.team_system = TeamSystem(event_bus=event_bus)
        self.spawning_system = SpawningSystem(event_bus=event_bus)
        self.vision_system = VisionSystem(event_bus=event_bus)
        self.movement_system = MovementSystem(event_bus=event_bus)

    def add_entity(self, entity_id:str , entity: Entity):
        self.all_entities[entity_id] = entity

    def remove_entity(self, entity_id: str):
        del self.all_entities[entity_id]

    def query(self, entity_id: str) -> Entity:
        return self.all_entities[entity_id]

    def render(self, display: pg.Surface):
        for render_system in self.render_systems:
            render_system.draw(display)