from __future__ import annotations
from in_game.ecs.components.component_base import Component
from typing import Tuple, List, TYPE_CHECKING, Any
from dataclasses import dataclass
import pygame as pg

if TYPE_CHECKING:
    from ecs.entity import Entity


@dataclass
class RectUIComponent(Component):
    size: tuple(int, int)
    image: pg.Surface | None = None
    outline: bool = True
    outline_color: tuple(int,int,int) = (255, 255, 255)
    outline_thickness: int = 1

@dataclass
class ClickableComponent(Component): ...






