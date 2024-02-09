from in_game.ecs.components.component_base import Component
from dataclasses import dataclass

@dataclass
class VisionComponent(Component):
    vision_radius: int
    is_blind: bool = False