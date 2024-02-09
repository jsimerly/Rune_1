from in_game.ecs.components.component_base import Component
from dataclasses import dataclass
from in_game.map.tile import GameTile
import pygame as pg

@dataclass
class ResourceComponent(Component):
    resource_name: str
    resource_color: tuple[int,int,int]
    max_resources: int
    min_resources: int
    end_of_turn_refresh: int
    bonus_type: str | None = None

