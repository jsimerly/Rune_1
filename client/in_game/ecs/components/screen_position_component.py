from in_game.ecs.components.component_base import Component
from typing import Tuple, List
import pygame as pg
from dataclasses import dataclass

@dataclass
class ScreenPositionComponent(Component):
    position: tuple[int, int] | None
    # def __init__(self, position: Tuple[int,int]):
    #     # if size: #get the top left of the component for drawing
    #     #     x_pos = position[0] - size[0]//2
    #     #     y_pos = position[1] - size[1]//2
    #     #     position = (x_pos, y_pos)
    #     self.position = position

