from components.sprite import SpriteComponent
import pygame as pg
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from map.game_tile import GameTile

class AbstractCharacter(ABC):
    def __init__(self, screen):
        self.sprite: SpriteComponent = None
        self.screen = screen

    def set_sprite_comp(self, comp: SpriteComponent):
        self.sprite = comp

    def open_image(self, image_path) -> pg.image:
        return pg.image.load(image_path).convert_alpha()
    
    def spawn_to_pixel_pos(self, pixel_pos:(int,int)):
        self.sprite.spawn_to_pixel(pixel_pos)
        


