from __future__ import annotations
from hex import Hex, Layout
from typing import Callable, Optional, List, TYPE_CHECKING, Set
from settings import LIGHT_GREY
import pygame as pg
from game.clickable_obj import AbstractClickableObject, ContinueClickAction
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
            return self._handle_initial_movement(self.tile.character)
        
        if self.tile.ghost_character:
            self.tile.ghost_character.movement.clear_move()
            return self._handle_initial_movement(self.tile.ghost_character)
                   
        
        self.tile.select()
        return self.next_click
    
    def _handle_initial_movement(self, character:AbstractCharacter):
            movement_options = character.movement.find_possible_tiles()
            for tile in movement_options:
                tile.set_option()
                self.prev_func_cache = movement_options

            self.tile.deselect()
            return self.second_movement_click

    def second_movement_click(self, passed_object: AbstractClickableObject):
        if self.tile.is_gametile_type(passed_object):
            if passed_object in self.prev_func_cache: #verify movement in range

                movement_path = self.tile.character.movement.astar(passed_object)
                if movement_path[-1].character:
                    print('Cannot move where another ontop of another character.')
                    return ContinueClickAction
                
                for tile in self.prev_func_cache:
                    tile.remove_option()

                if passed_object == self.tile.character.current_tile:
                    self.tile.deselect()
                    self.tile.character.movement.clear_move()
                    
                    return None
                
                self.tile.character.movement.move(movement_path)
                return None
            else:
                update_tiles: Set[GameTile] = set()
                for tile in self.prev_func_cache:
                    neighbors = tile.get_all_neighbor_tiles()
                    update_tiles.update(neighbors)

                for tile in update_tiles:
                    tile.remove_option()
                self.tile.game_map.render.add_borders(self.prev_func_cache)
                print('Cannot move there')
                return None

        self.prev_func_cache = None
        return None     
    
    def next_click(self, passed_obj: AbstractClickableObject) -> Optional[Callable]:
        self.tile.deselect()
        self.tile.register_neighor_border_render()
        next_function = passed_obj.on_click()
        return next_function