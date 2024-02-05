from in_game.ecs.components.component_base import Component
from typing import Tuple, List
import pygame as pg

class VisualHexEdgeComponent(Component):
    def __init__(self, 
        verticies:List[Tuple[int,int]], 
        thickness:int=1, 
        color=(160,160,160),
        transparent=False,
    ):
        self.verticies = verticies
        self.thickness = thickness
        self.color = color
        self.transparent=transparent

class SelectedHexEdgeComponent(Component):
    def __init__(self, 
        verticies:List[Tuple[int,int]], 
        thickness:int=4, 
        color=(255,255,255),
    ):
        self.verticies = verticies
        self.thickness = thickness
        self.color = color

