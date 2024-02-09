from in_game.ecs.components.component_base import Component
from dataclasses import dataclass, field
from in_game.map.tile import GameTile
import pygame as pg

@dataclass
class ResourceComponent:
    name: str
    color: tuple[int, int, int]
    max: int
    min: int
    end_of_turn_refresh: int
    amount: int = field(default=None)  # Set a placeholder default value
    bonus_type: str | None = None

    def __post_init__(self):
        if self.amount is None:
            self.amount = self.end_of_turn_refresh

