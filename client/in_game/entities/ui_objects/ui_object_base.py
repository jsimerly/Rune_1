from typing import List
from in_game.ecs.components.component_base import Component
from in_game.ecs.components.ui_components import RectUIComponent, ClickableComponent
from in_game.ecs.components.screen_position_component import ScreenPositionComponent
from in_game.ecs.components.spawner_component import TriggerSpawningComponent
from in_game.ecs.entity import Entity
from abc import abstractmethod
import pygame as pg


class UIObject(Entity):
    required_components = [ScreenPositionComponent]

    def __init__(self, entity_id, components: List[Component] = None) -> None:
        super().__init__(entity_id, components)

class RectUIObject(UIObject):
    required_components = [RectUIComponent, ScreenPositionComponent]


class ButtonObject(RectUIObject):
    required_components = [ClickableComponent]


class SpawningButton(ButtonObject):
    size = (100, 100)
    outline_color = (255, 255, 255)
    outline_thickness = 2
    required_components = [TriggerSpawningComponent]

    def __init__(self, entity_id, image, position, spawning_entity_id:str) -> None:
        clickable_component = ClickableComponent()
        image = pg.transform.scale(image, self.size)
        rect_ui_component = RectUIComponent(
            self.size, image, 
            outline=True, 
            outline_color=self.outline_color, 
            outline_thickness=self.outline_thickness
        )
        screen_position_component = ScreenPositionComponent(position)
        trigger_spawn_component = TriggerSpawningComponent(spawning_entity_id)

        components = [
            clickable_component, 
            rect_ui_component, 
            screen_position_component,
            trigger_spawn_component,
        ]
        super().__init__(entity_id, components)

