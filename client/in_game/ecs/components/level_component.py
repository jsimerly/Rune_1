from in_game.ecs.components.component_base import Component
from dataclasses import dataclass


@dataclass
class LevelComponent(Component):
    level: int = 1
    max_level: int = 3
    xp: int = 0
    xp_to_next: int = 1000
