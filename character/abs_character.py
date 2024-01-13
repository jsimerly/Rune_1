from __future__ import annotations
from components.sprite import SpriteComponent
from components.movement import MovementComponent
import pygame as pg
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, List
from client.surfaces import GameSurfaces
if TYPE_CHECKING:
    from map.game_tile import GameTile
    from team.team import Team



class AbstractCharacter(ABC):    
    def __init__(self, surface):
        self.game_surfaces = GameSurfaces()
        self.team: Team = None
        self.current_tile: GameTile = None

        self.sprite: SpriteComponent = None
        self.movement: MovementComponent = None
        self.surface = surface
        self.color = None

    ''' Movement '''
    def move_to_tile(self, tile: GameTile) -> List[GameTile]:
        if not self.movement.queue.is_empty:
            self.movement.clear_move()
        queue = self.movement.move(tile)
        return queue

    def remove_from_tile(self):
        self.current_tile.remove_character()
        self.current_tile = None
        self.sprite.undraw()
    
    def set_team(self, team:Team):
        self.team = team

    def set_sprite_comp(self, image: pg.Surface):
        self.sprite = SpriteComponent(image)

    def set_movement_comp(self):
        self.movement = MovementComponent(self)

    def set_color(self, color: (int,int,int)):
        self.color = color

    def open_image(self, image_path) -> pg.image:
        return pg.image.load(image_path).convert_alpha()
    
    def spawn_to_pixel_pos(self, tile:GameTile):
        self.sprite.spawn_to_pixel(tile)
        


