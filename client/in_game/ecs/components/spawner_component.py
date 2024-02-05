from in_game.ecs.components.component_base import Component
from dataclasses import dataclass


@dataclass
class SpawnerComponent(Component):
    radius: int

@dataclass
class TriggerSpawningComponent(Component): ...

@dataclass
class SpawningComponent(Component): ...
