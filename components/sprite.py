from __future__ import annotations
from .abstact_component import AbstactComponent
import pygame as pg
from typing import TYPE_CHECKING, List, Optional
import time
if TYPE_CHECKING:
    from map.game_tile import GameTile

class SpriteComponent(AbstactComponent):
    NORMAL_SIZE = (60,60)
    GHOST_ALPHA = 100

    def __init__(self, image: pg.image, surface: pg.Surface):
        self.surface = surface

        self.image = pg.transform.scale(image, self.NORMAL_SIZE)
        self.ghost_image = self.image.copy()
        self.ghost_image.set_alpha(self.GHOST_ALPHA)

    def get_topleft_pos(self, tile_center_pixel: (int,int)) -> (int, int):
        x, y = tile_center_pixel

        x -= self.NORMAL_SIZE[0] // 2
        y -= self. NORMAL_SIZE[1] // 2
        return ((x,y))

    def draw(self, pixel_pos: (int, int)):
        top_left_pixel = self.get_topleft_pos(pixel_pos)
        self.surface.blit(self.image, top_left_pixel)

    def draw_ghost(self, pixel_pos: (int, int)):
        top_left_pixel = self.get_topleft_pos(pixel_pos)
        self.surface.blit(self.ghost_image, top_left_pixel)
