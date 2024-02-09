from in_game.ecs.components.component_base import Component
from dataclasses import dataclass

@dataclass
class FogOfWarComponent(Component):
    is_fog_of_war: bool = True