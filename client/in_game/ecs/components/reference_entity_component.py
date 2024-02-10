from in_game.ecs.components.component_base import Component
from dataclasses import dataclass
import pygame as pg

@dataclass
class ReferenceEntityComponent(Component):
    entity_id: str