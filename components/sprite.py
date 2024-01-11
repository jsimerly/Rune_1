from __future__ import annotations
from .abstact_component import AbstactComponent
import pygame as pg
from typing import TYPE_CHECKING, List, Optional
import time
if TYPE_CHECKING:
    from map.game_tile import GameTile

class SpriteComponent(AbstactComponent):
    NORMAL_SIZE = (55,55)
    GHOST_ALPHA = 100

    def __init__(self, image: pg.image, char_surface: pg.Surface):
        self.char_surface = char_surface
        self.pixel_pos: (int,int) = None

        self.standard_image = pg.transform.scale(image, self.NORMAL_SIZE)
        self.ghost_image = self.standard_image.copy()
        self.ghost_image.set_alpha(self.GHOST_ALPHA)
        self.empty = pg.Color(0,0,0,0)


    def get_topleft_pos(self, tile_center_pixel: (int,int)) -> (int, int):
        x, y = tile_center_pixel

        x -= self.NORMAL_SIZE[0] // 2
        y -= self. NORMAL_SIZE[1] // 2
        return ((x,y))

    def draw(self, pixel_pos: (int, int)):
        self.pixel_pos = pixel_pos
        top_left_pixel = self.get_topleft_pos(pixel_pos)
        self.char_surface.blit(self.standard_image, top_left_pixel)
        

    def undraw(self, pixel_pos: (int,int)=None):
        pixel_pos = pixel_pos if pixel_pos else self.pixel_pos
        top_left_pixel = self.get_topleft_pos(self.pixel_pos)
        rect_to_clear = pg.Rect(top_left_pixel, self.NORMAL_SIZE)
        self.char_surface.fill(self.empty, rect_to_clear)