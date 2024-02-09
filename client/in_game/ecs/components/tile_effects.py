from in_game.ecs.components.component_base import Component
from dataclasses import dataclass
import pygame as pg

@dataclass
class VisualTileEffect(Component):
    image: pg.Surface | None
    color: tuple[int, int, int] | None
    transparency: bool
