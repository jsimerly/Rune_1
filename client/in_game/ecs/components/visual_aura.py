from in_game.ecs.components.component_base import Component
from dataclasses import dataclass
import pygame as pg

@dataclass
class VisualAuraComponent(Component):
    radius: int
    color: tuple[int, int, int] | None
    transparency_value: int
    tapering_intensity: int = 0