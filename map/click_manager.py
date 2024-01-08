from __future__ import annotations
from hex import Hex, Layout
from typing import Callable, Optional, List, TYPE_CHECKING
from settings import LIGHT_GREY
import pygame as pg
from game.clickable_obj import AbstractClickableObject
from game.game_phase import GamePhase
from components.map_interaction import MapInteractionComponent
import time
if TYPE_CHECKING:
    from character.abs_character import AbstractCharacter
    from game_map import GameMap
    from game.brock_purdy import GamePhaseManager
    from .game_tile import GameTile

#Using this as a facade for click events as they were bloating the gametile class and all events run through game tile selection.
class ClickManager:
    def __init__(self, parent_tile: GameTile):
        self.prev_func_cache = None
        self.in_click_chain = False
        self.tile = parent_tile

    def on_click(self) -> Callable:
        return self.router()
    
    def router(self):
        current_phase = self.tile.game_manager.current_phase
        if current_phase == GamePhase.MOVE_QUEUEING:
            return self.initial_movement_click()
        
        self.tile.select()
        return self.next_click

    def initial_movement_click(self):
        if self.tile.character:
            movement_options = self.tile.character.movement.find_possible_tiles()
            for tile in movement_options:
                tile.draw_border(border_color=(200, 200, 200), border_thickness=3)
                self.prev_func_cache = movement_options

            self.tile.deselect()
            return self.second_movement_click
        
        self.tile.select()
        return self.next_click
        
    def second_movement_click(self, passed_object: AbstractClickableObject):
        self.tile.game_map.redraw_tile_borders(self.prev_func_cache)
        if isinstance(passed_object, type(self.tile)):
            if passed_object in self.prev_func_cache:
                if passed_object == self.tile.character.current_tile:
                    self.tile.deselect()
                    print('Deselected.')
                    return None
                movement_path = self.tile.character.movement.astar(passed_object)
                self.tile.game_map.draw_movement_path(movement_path)
                self.tile.character.movement.move(movement_path)
                
            else:
                print('Cannot move there')

        self.prev_func_cache = None
        return None     
    
    def next_click(self, passed_obj: AbstractClickableObject) -> Optional[Callable]:
        self.tile.deselect()
        self.tile.redraw_neighbors_borders()
        next_function = passed_obj.on_click()
        return next_function