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

    def __init__(self, image: pg.image, screen):
        self.is_selected = False
        self.screen = screen
        self.tile: GameTile = None
        self.image = pg.transform.scale(image, self.NORMAL_SIZE)

        self.ghost_tile: GameTile = None
        self.ghost_image = self.image.copy()
        self.ghost_image.set_alpha(self.GHOST_ALPHA)

    def get_topleft_pos(self, ghost=False) -> (int, int):
        if ghost:
            x,y = self.ghost_tile.get_center_pixel()
        else:
            x, y = self.tile.get_center_pixel()

        x -= self.NORMAL_SIZE[0] // 2
        y -= self. NORMAL_SIZE[1] // 2
        return ((x,y))

    def spawn_to_pixel(self, tile: GameTile):
        self.tile = tile
        self.draw_tile()

    def draw_tile(self):
        top_left_pixel = self.get_topleft_pos()
        self.screen.blit(self.image, top_left_pixel)

    def ghost_to_pixel(self, tile):
        self.ghost_tile = tile
        self.draw_ghost()

    def draw_ghost(self):
        top_left_pixel = self.get_topleft_pos(ghost=True)
        self.screen.blit(self.ghost_image, top_left_pixel)

    def draw_movement_queue(self, queued_movement: Optional[List[GameTile]]):
        if not queued_movement:
            self.tile.draw()
            self.ghost_tile.draw()
            self.tile = self.ghost_tile
            self.ghost_tile = None
            self.draw_tile()
            return
        self.ghost_tile = queued_movement[0]
        self.tile = queued_movement[-1]
        self.ghost_tile.draw()
        self.draw_ghost()
        self.draw_tile()

    def draw_movement_dequeue(self):
        self.tile.draw()
        self.ghost_tile.draw()

        self.tile = self.ghost_tile
        self.ghost_tile = None




