from __future__ import annotations
from hex import Hex, Layout
from typing import Callable, Optional, List, TYPE_CHECKING, Set
from settings import LIGHT_GREY
import pygame as pg
from game.clickable_obj import AbstractClickableObject, ContinueClickAction, AbstactDraggableObj
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
        self.tile: GameTile = parent_tile

    def on_click(self) -> Callable:
        if self.tile.character: #will soon handle abilities too
            if not self.tile.character.movement.queue.is_empty:
                print('handle ability')
                return self.next_click
            else:
                char_holder = self.tile.character
                self.tile.character.movement.clear_move()
                return self._handle_initial_movement(char_holder)
        
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
            return character.current_tile.click_manager.second_click

    def second_click(self, passed_object: AbstractClickableObject):
        if self.tile.is_gametile_type(passed_object):
            if passed_object in self.prev_func_cache: #verify movement in range
                could_complete = self.tile.character.movement.click_move(passed_object)

                if could_complete:
                    self.tile.deselect()
                    for tile in self.prev_func_cache:
                        tile.remove_option()

                    return None

                could_complete = self.tile.character.movement.click_move(passed_object)
                if not could_complete:
                    return ContinueClickAction
            
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
    

    '''
        Dragging
    '''
    def on_drag_start(self) -> Optional[Callable]:
        if self.tile.character and self.tile.character.movement.queue():
            return self.drag_move_update, self.tile.character

        if self.tile.character:
            return self.drag_spawn_update, self.tile.character
        
        if self.tile.ghost_character:
            return self.drag_spawn_update, self.tile.character
        
        return None, None

    def drag_spawn_update(self, mouse_pos, character: AbstractCharacter):
        character.current_tile.character = None
        character.sprite.draw(mouse_pos)
            
        return self.drag_spawn_update

    def drag_move_update(self):
        pass

    def drag_ability_update(self):
        pass

    def drag_spawn_finish(self, final_tile: GameTile, character: AbstractCharacter,):
        character.current_tile.remove_character()
        final_tile.add_character(character)

    def on_drag_finish(self) -> Optional[Callable]:
        pass
    

    
