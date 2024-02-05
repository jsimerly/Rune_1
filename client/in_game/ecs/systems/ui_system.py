from __future__ import annotations

from in_game.ecs.entity import Entity
from in_game.event_bus import EventBus
from .system_base import System
from in_game.ecs.components.sprite_component import TileSpriteComponent, SpriteComponent
from in_game.ecs.components.visual_edge_component import VisualHexEdgeComponent, SelectedHexEdgeComponent
from in_game.ecs.components.screen_position_component import ScreenPositionComponent
from in_game.map.tile import GameTile
from typing import Optional
import pygame as pg
from abc import abstractmethod

from typing import TYPE_CHECKING, Tuple

if TYPE_CHECKING:
    from entity import Entity

class UISystem(System):
    required_components = [RectUIComponent]
    def draw(self, display: pg.Surface):
        for entity in self.entities:
            self.draw_entity(display, entity)

    def draw_entity(self, display: pg.Surface, entity: Entity):
        entity
