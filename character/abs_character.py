from __future__ import annotations
from components.sprite import SpriteComponent
from components.movement import MovementComponent
import pygame as pg
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
from enum import Enum
if TYPE_CHECKING:
    from map.game_tile import GameTile
    from team.team import Team


class LifeState(Enum):
    AWAITING_SPAWN = 1
    ALIVE = 2
    DEAD = 3
class AbstractCharacter(ABC):
    def __init__(self, surface):
        self.team: Team = None
        self.current_tile: GameTile = None

        self.sprite: SpriteComponent = None
        self.movement: MovementComponent = None
        self.surface = surface
        self.color = None

        self.life_states = LifeState
        self.life_state = self.life_states.AWAITING_SPAWN

    def remove_from_tile(self):
        self.current_tile.remove_character()
        self.current_tile = None
        self.sprite.undraw()
        print('removed??')
    
    def set_team(self, team:Team):
        self.team = team

    def set_sprite_comp(self, comp: SpriteComponent):
        self.sprite = comp

    def set_movement_comp(self, comp: MovementComponent):
        self.movement = comp

    def set_color(self, color: (int,int,int)):
        self.color = color

    def open_image(self, image_path) -> pg.image:
        return pg.image.load(image_path).convert_alpha()
    
    def spawn_to_pixel_pos(self, tile:GameTile):
        self.sprite.spawn_to_pixel(tile)
        


