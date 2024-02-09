from in_game.ecs.components.component_base import Component
from typing import Tuple, List
import pygame as pg

class VisualHexEdgeComponent(Component):
    def __init__(self, 
        verticies:List[Tuple[int,int]], 
        transparent=False
    ):
        self.default_thickness = 1
        self.default_color = (140,140,140)
        self.default_transparency=transparent

        self.verticies = verticies
        self.thickness = self.default_thickness
        self.color = self.default_color
        self.transparent= self.default_transparency

class SelectedHexEdgeComponent(Component):
    def __init__(self, 
        verticies:List[Tuple[int,int]], 
        thickness:int=4, 
        color=(255,255,255),
    ):
        self.verticies = verticies
        self.thickness = thickness
        self.color = color

