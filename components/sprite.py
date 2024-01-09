from __future__ import annotations
from .abstact_component import AbstactComponent
import pygame as pg
from typing import TYPE_CHECKING, List
import time
if TYPE_CHECKING:
    from map.game_tile import GameTile

class SpriteComponent(AbstactComponent):
    NORMAL_SIZE = (60,60)
    GHOST_ALPHA = 100

    def __init__(self, image: pg.image, screen):
        self.is_selected = False
        self.screen = screen
        self.pixel_pos = None
        self.image = pg.transform.scale(image, self.NORMAL_SIZE)

        self.ghost_pixel_pos = None
        self.ghost_image = self.image.copy()
        self.ghost_image.set_alpha(self.GHOST_ALPHA)

    def get_topleft_pos(self, ghost=False) -> (int, int):
        if ghost:
            x,y = self.ghost_pixel_pos
        else:
            x, y = self.pixel_pos

        x -= self.NORMAL_SIZE[0] // 2
        y -= self. NORMAL_SIZE[1] // 2
        return ((x,y))

    def spawn_to_pixel(self, pixel):
        self.pixel_pos = pixel
        self.draw()

    def draw(self):
        top_left_pixel = self.get_topleft_pos()
        self.screen.blit(self.image, top_left_pixel)

    def ghost_to_pixel(self, pixel):
        self.ghost_pixel_pos = pixel
        self.draw_ghost()

    def draw_ghost(self):
        top_left_pixel = self.get_topleft_pos(ghost=True)
        self.screen.blit(self.ghost_image, top_left_pixel)

    def draw_movement_queue(self, from_tile: GameTile, to_tile: GameTile):
        self.ghost_pixel_pos = from_tile.get_center_pixel()
        self.pixel_pos = to_tile.get_center_pixel()

        from_tile.draw()
        to_tile.draw()
        self.draw_ghost()
        self.draw()

    def draw_movement_dequeue(self, from_tile: GameTile, to_tile:GameTile):
        self.pixel_pos = self.ghost_pixel_pos
        self.ghost_pixel_pos = None

        from_tile.draw()
        to_tile.draw()
        self.draw()



