from __future__ import annotations
from components.sprite import SpriteComponent
from components.movement import MovementComponent
import pygame as pg
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, List, Tuple
from client.surfaces import GameSurfaces
if TYPE_CHECKING:
    from map.game_tile import GameTile
    from team.team import Team



class AbstractCharacter(ABC):    
    def __init__(self):
        self.team: Team = None
        self.current_tile: GameTile = None

        self.sprite: SpriteComponent = None
        self.movement: MovementComponent = None
        self.color = None
        self.surfaces = GameSurfaces()

    '''Set Up'''
    def set_team(self, team:Team):
        self.team = team

    def set_sprite_comp(self, image: pg.Surface):
        self.sprite = SpriteComponent(image)

    def set_movement_comp(self):
        self.movement = MovementComponent(self)

    def set_color(self, color: Tuple(int,int,int)):
        self.color = color
        print(color)

    def open_image(self, image_path) -> pg.image:
        return pg.image.load(image_path).convert_alpha()

    ''' Movement '''
    def move_to_tile(self, tile: GameTile):
        if not self.movement.queue.is_empty:
            self.movement.clear_move()
        self.movement.move(tile)

    def remove_from_tile(self):
        self.current_tile.remove_character()
        self.current_tile = None
    
    def spawn_to(self, tile:GameTile):
        self.current_tile = tile
        self.sprite.move_to_pixel(tile.center_pixel)
        self.surfaces.add_to_layer(self.surfaces.characters, obj=self)

    def die(self):
        self.current_tile = None
        self.surfaces.remove_from_layer(self.surfaces.characters, obj=self)

    '''Drawing'''
    def draw(self, screen: pg.Surface):
        self.sprite.draw(screen) # pass the tile 
        self.sprite.draw_ghost(screen) # pass the ghost tile


