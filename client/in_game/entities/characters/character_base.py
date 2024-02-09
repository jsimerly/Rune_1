from __future__ import annotations
from typing import List, TYPE_CHECKING, Optional, Union
from in_game.ecs.components.component_base import Component

from in_game.ecs.components.sprite_component import SpriteComponent
from in_game.ecs.entity import Entity
from in_game.ecs.components.occupier_component import OccupierComponent
from in_game.ecs.components.screen_position_component import ScreenPositionComponent
from in_game.ecs.components.team_component import TeamComponent
from in_game.ecs.components.name_component import NameComponent
import pygame as pg

if TYPE_CHECKING:
    from in_game.ecs.components.component_base import Component


class Character(Entity):
    required_components = [
        SpriteComponent,
        OccupierComponent,
        ScreenPositionComponent,
        TeamComponent,
        NameComponent,
    ]
    size = (75, 75)

    def __init__(self, entity_id:str, name:str, sprite: pg.Surface, team_id: str, is_team_1:bool) -> None:
        name_component = NameComponent(name)
        y_offset = int(self.size[1] * .3)
        sprite_components = SpriteComponent(sprite, self.size, y_offset=y_offset)
        screen_position_component = ScreenPositionComponent(None)
        team_component = TeamComponent(team_id, is_team_1)
        occupier_component = OccupierComponent(None)

        components = [
            name_component,
            sprite_components,
            screen_position_component,
            team_component,
            occupier_component,
        ]
        super().__init__(entity_id=entity_id, components=components)



