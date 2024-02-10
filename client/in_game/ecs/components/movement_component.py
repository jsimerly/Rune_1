from in_game.ecs.components.component_base import Component
from dataclasses import dataclass, field
from in_game.map.tile import GameTile
import pygame as pg

@dataclass
class MovementComponent(Component):
    cost: int
    line_color: tuple[int,int,int] 
    start_tile: GameTile = None #this will need to be reset after every turn with update from server
    queue: list[GameTile] = field(default_factory=list)
    line_width: int = 3
