from __future__ import annotations
from .abstact_component import AbstactComponent
import pygame as pg
from typing import TYPE_CHECKING, List, Optional
# from in_game.surfaces import GameSurfaces
import time
if TYPE_CHECKING:
    from map.game_tile import GameTile

class SpriteComponent(AbstactComponent):
    NORMAL_SIZE = (55,55)
    GHOST_ALPHA = 100

    def __init__(self, image: pg.image):
        self.pixel_pos: (int,int) = None
        self.ghost_pos: (int, int) = None

        self.standard_image = pg.transform.scale(image, self.NORMAL_SIZE)
        self.ghost_image = self.standard_image.copy()
        self.ghost_image.set_alpha(self.GHOST_ALPHA)
        self.empty = pg.Color(0,0,0,0)

        self.dead_image = None # used for when they die


    def get_topleft_pos(self, tile_center_pixel: (int,int)) -> (int, int):
        x, y = tile_center_pixel

        x -= self.NORMAL_SIZE[0] // 2
        y -= self. NORMAL_SIZE[1] // 2
        return ((x,y))
    
    def move_to_tile(self, tile: GameTile):
        pixel_pos = self.get_topleft_pos(tile.center_pixel)
        self.pixel_pos = pixel_pos

    def ghost_to_tile(self, tile: GameTile):
        pixel_pos = self.get_topleft_pos(tile.center_pixel)
        self.ghost_pos = pixel_pos
    
    def move_to_pixel(self, center_pixel_pos: (int,int)):
        pixel_pos = self.get_topleft_pos(center_pixel_pos)
        self.pixel_pos = pixel_pos

    def ghost_to_pixel(self, center_pixel_pos: (int, int)):
        pixel_pos = self.get_topleft_pos(center_pixel_pos)
        self.ghost_pos = pixel_pos

    def remove_sprite(self):
        self.pixel_pos = None

    def remove_ghost(self):
        self.ghost_pos = None

    def draw(self, screen: pg.Surface):
        if self.pixel_pos:
            screen.blit(self.standard_image, self.pixel_pos)

    def draw_ghost(self, screen: pg.Surface):
        if self.ghost_pos:
            screen.blit(self.ghost_image,self.ghost_pos)
        


        