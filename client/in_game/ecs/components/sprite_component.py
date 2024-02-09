from in_game.ecs.components.component_base import Component
from typing import Tuple, List
import pygame as pg

class SpriteComponent(Component):
    def __init__(self, 
        raw_image: pg.Surface, size:Tuple[int,int], y_offset: int=0
    ):
        image = pg.transform.scale(raw_image, size)
        self.image: pg.Surface = image
        self.y_offset = y_offset
        self.is_visible = True

class TileSpriteComponent(SpriteComponent):
    def __init__(self, 
    raw_image: pg.Surface, bg_color:Tuple[int,int], verticies: List[Tuple[int,int]], size: Tuple[int, int], pos: Tuple[int, int]):
        self.bg_color = bg_color
        self.verticies = verticies

        if raw_image:
            image_size = (int(size[0]*1.5), int(size[1]*1.5))
            image = pg.transform.scale(raw_image, image_size)
            self.image: pg.Surface = image
        else:
            self.image = None
        self.is_visible = True
class VisualTileAffectComponent(Component):
    def __init__(self,
        raw_image: pg.Surface, 
        color: tuple[int,int,int], 
        is_transparent: bool,
        size: tuple[int,int,int]
    ) -> None:
        self.color = color
        self.is_transparent=is_transparent
        if raw_image:
            image_size = (int(size[0]*1.5), int(size[1]*1.5))
            image = pg.transform.scale(raw_image, image_size)
            self.image: pg.Surface = image
        else:
            self.image = None
        
        

