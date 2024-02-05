from __future__ import annotations
from typing import List, TYPE_CHECKING, Optional, Union
from in_game.ecs.components.component_base import Component

from in_game.ecs.components.sprite_component import SpriteComponent
from in_game.ecs.entity import Entity
from in_game.ecs.components.occupier_component import OccupierComponent
from in_game.ecs.components.screen_position_component import ScreenPositionComponent
from in_game.ecs.components.team_component import TeamComponent
import pygame as pg

if TYPE_CHECKING:
    from in_game.ecs.components.component_base import Component


class Character(Entity):
    required_components = [
        SpriteComponent,
        OccupierComponent,
        ScreenPositionComponent,
        TeamComponent
    ]

    def __init__(self, components: List[Component] = None) -> None:
        super().__init__(components)



