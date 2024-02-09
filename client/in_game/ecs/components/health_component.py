from in_game.ecs.components.component_base import Component
from dataclasses import dataclass, field
from in_game.map.tile import GameTile
import pygame as pg

@dataclass
class HealthComponent(Component):
    max: int
    current: int
