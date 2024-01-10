from __future__ import annotations
from components.sprite import SpriteComponent
from components.movement import MovementComponent
import pygame as pg
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from map.game_tile import GameTile
    from team.team import Team
class AbstractCharacter(ABC):
    def __init__(self, screen, game_map):
        self.current_tile = None
        self.team = None
        self.sprite: SpriteComponent = None
        self.movement: MovementComponent = None
        self.screen = screen
        self.game_map = game_map

    def set_team(self, team:Team):
        self.team = team

    def set_sprite_comp(self, comp: SpriteComponent):
        self.sprite = comp

    def set_movement_comp(self, comp: MovementComponent):
        self.movement = comp

    def open_image(self, image_path) -> pg.image:
        return pg.image.load(image_path).convert_alpha()
    
    def spawn_to_pixel_pos(self, tile:GameTile):
        self.sprite.spawn_to_pixel(tile)
        


