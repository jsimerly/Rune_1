from typing import List
from client.in_game.ecs.components.component_base import Component
from client.in_game.ecs.components.ui_components import RectUIComponent, ClickableComponent
from in_game.ecs.components.screen_position_component import ScreenPositionComponent
from in_game.ecs.entity import Entity
from abc import abstractmethod
import pygame as pg


class UIObject(Entity):
    required_components = [ScreenPositionComponent]

    def __init__(self, components: List[Component] = None) -> None:
        super().__init__(components)


class RectUIObject(UIObject):
    required_components = [RectUIComponent, ScreenPositionComponent]

    def __init__(self, components: List[Component] = None) -> None:
        super().__init__(components)


class ButtonObject(RectUIObject):
    required_components = [ClickableComponent]


class SpawningButtonComponent(ButtonObject):
    required_components = [SpawnerComponent]

    def __init__(self, components: List[Component] = None) -> None:
        super().__init__(components)

