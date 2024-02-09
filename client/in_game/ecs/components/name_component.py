from in_game.ecs.components.component_base import Component
from dataclasses import dataclass

@dataclass
class NameComponent:
    name: str