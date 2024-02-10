from in_game.ecs.components.component_base import Component
from dataclasses import dataclass, field
from in_game.map.tile import GameTile
import pygame as pg

@dataclass
class MovementComponent(Component):
    movement_cost: int
    ghost_image: pg.Surface
    movement_line_color: tuple[int,int,int] 
    start_tile: GameTile = None
    movement_queue: list[GameTile] = field(default_factory=list)
    line_width: int = 3
