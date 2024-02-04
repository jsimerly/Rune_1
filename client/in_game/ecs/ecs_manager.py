from __future__ import annotations
from .systems.render_systems import DrawSpriteSystem, DrawTileSystem, DrawHexEdgeSystem
from .systems.render_systems import RenderSystem
from .systems.occupancy_systems import OccupancySystem
from .systems.team_system import TeamSystem
from typing import TYPE_CHECKING, List
import pygame as pg

if TYPE_CHECKING:
    from map.map import GameMap

class ECSManager:
    def __init__(self) -> None:
        ''' Rendering Systems'''
        self.tile_sprite_system = DrawTileSystem()
        self.border_system = DrawHexEdgeSystem()
        self.selected_system = DrawHexEdgeSystem()
        self.building_sprite_system = DrawSpriteSystem()
        self.objective_sprite_system = DrawSpriteSystem()
        #movement lines
        self.character_sprite_system = DrawSpriteSystem()
        #ability system

        self.render_systems: List[RenderSystem] = [
            self.tile_sprite_system,
            self.border_system,
            self.selected_system,
            self.building_sprite_system,
            self.objective_sprite_system,
            #
            self.character_sprite_system,
            #
        ]

        ''''''
        self.occupancy_system = OccupancySystem()
        self.team_system = TeamSystem()


    def render(self, display: pg.Surface):
        for render_system in self.render_systems:
            render_system.draw(display)