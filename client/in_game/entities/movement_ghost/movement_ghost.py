from typing import List
from in_game.ecs.components.component_base import Component
from in_game.ecs.components.occupier_component import OccupierComponent
from in_game.ecs.components.reference_entity_component import ReferenceEntityComponent
from in_game.ecs.components.sprite_component import SpriteComponent
from in_game.ecs.components.screen_position_component import ScreenPositionComponent
from in_game.ecs.entity import Entity
import pygame as pg


class MovementGhost(Entity):
    def __init__(self, entity_id: str, image: pg.Surface, id_of_main_entity: str) -> None:
        occupier_component = OccupierComponent()
        screen_position_component = ScreenPositionComponent()
        sprite_component = SpriteComponent(image, image.get_size())
        reference_component = ReferenceEntityComponent(id_of_main_entity)
        components = [
            occupier_component, 
            screen_position_component, 
            reference_component,
            sprite_component,
        ]
        super().__init__(entity_id, components)