from __future__ import annotations
from components.sprite import SpriteComponent
from components.movement import MovementComponent
from components.map_interaction import MapInteractionComponent
from components.leveling import LevelingComponent
import pygame as pg
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, List, Tuple
from zclient.surfaces import GameSurfaces
if TYPE_CHECKING:
    from map.game_tile import GameTile
    from team.team import Team

class AbstractCharacter(ABC):    
    def __init__(self, image: pg.Surface, color:Tuple[int,int,int]):
        self.current_tile: GameTile = None
        self.team = None
        self.color = color
        self.surfaces = GameSurfaces()
        self.speed = 50
        self.stength = 50

        '''fix max drag distance when you create resoucing component'''
        self.sprite: SpriteComponent = SpriteComponent(image)
        self.movement: MovementComponent = MovementComponent(color)
        self.leveling: LevelingComponent = LevelingComponent()
        self.map_interaction: MapInteractionComponent = MapInteractionComponent(
            is_passable = True,
            can_pierce = True,
            can_end_on = False,
            blocks_vision = False,
            hides_occupants = False,
            is_slowing = False,
            walkthrough_effects = None,
        )


    '''Set Up'''
    def set_team(self, team: Team):
        self.team = team

    def set_sprite_comp(self, image: pg.Surface):
        self.sprite = SpriteComponent(image)

    def set_movement_comp(self):
        self.movement = MovementComponent(self.color)

    def set_leveling_comp(self):
        self.leveling = LevelingComponent()

    def set_color(self, color: Tuple(int,int,int)):
        self.color = color

    def open_image(self, image_path) -> pg.image:
        return pg.image.load(image_path).convert_alpha()

    ''' Movement '''
    def move_to_tile(self, tile: GameTile):
        if not self.movement.queue.is_empty:
            self.clear_move()
        self.movement.move(self.current_tile, tile)
        self.sprite.move_to_tile(tile)
        self.sprite.ghost_to_tile(self.current_tile)
        self.current_tile.character_move_to(tile)

    def drag_move_start(self):
        self.clear_move()
        self.drag_move(self.current_tile)
        self.sprite.ghost_to_tile(self.current_tile)

    def drag_move(self, tile: GameTile):
        self.movement.drag_move_new_tile(tile)
        self.sprite.move_to_tile(tile)

    def drag_move_finish(self, final_tile: GameTile):
        self.current_tile = final_tile

    def clear_move(self):
        start_tile, end_tile = self.movement.clear_move()
        if end_tile:
            end_tile.remove_character()

        if start_tile:
            self.current_tile = start_tile
            self.sprite.move_to_tile(start_tile)

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

    '''Processing'''
    def process_next_move(self) -> bool:
        if not self.movement.queue.is_empty:
            next_tile = self.movement.queue.queue.pop(0)
            next_tile.process_character_walkthrough(self)

            if self.movement.queue.is_empty:
                self.current_tile = next_tile
                return False

            return True
        return False
                

    '''Drawing'''
    def draw(self, screen: pg.Surface):
        self.sprite.draw(screen)
        self.sprite.draw_ghost(screen)
        if self.current_tile:
            x, y = self.current_tile.center_pixel
            x += 15
            y -= 30
            self.leveling.draw(screen, pixel_pos=(x,y))

    def draw_movement(self, screen: pg.Surface):
        pass


    

