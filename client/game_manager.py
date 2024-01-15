from __future__ import annotations
from .ui.buttons.button import ButtonManager, Button
from .clickable_obj import Clickable, Draggable, ContinueAction
from typing import List, Dict, Callable, TYPE_CHECKING, Optional, Tuple
from client.action_state.action_state import IdleState, ActionState, MouseInput, ActionContext
import pygame as pg
from client.surfaces import GameSurfaces
from client.ui.buttons.button import ButtonManager
from client.ui.buttons.spawn_button import SpawnButton
if TYPE_CHECKING:
    from map.loadouts.map_layout import MapLayout
    from character.abs_character import AbstractCharacter
    from map.game_tile import GameTile


class GameManager:
    '''
        This is the client side game manager that will hold the state of all objects and manage clicks within the game board and UI. 
    '''
    def __init__(self, map: MapLayout, screen: pg.Surface):
        self.button_manager = ButtonManager() #event manager for buttons
        self.surfaces = GameSurfaces(screen=screen)
        self.layout = map.layout

        self.tiles: Dict[Tuple[int,int], GameTile] = map.generate_map()
        for tile in self.tiles.values():
            tile.set_tile_map(self.tiles)
            self.surfaces.add_to_layer(self.surfaces.standard_tiles, tile)

            if tile.building:
                self.surfaces.add_to_layer(self.surfaces.buildings, tile.building)

        self.characters: List[AbstractCharacter] = []
        self.buildings = []
        self.enemy_characters: List[AbstractCharacter] = []
        self.enemy_buildings = []

        self.leveling_stones = []
        self.leveling_shards = []
        self.altars = []

        self.action_context = ActionContext()
        self.action_state = IdleState(self)

    '''Register Events'''
    def register_button(self, button: Button):
        self.button_manager.register(button)

    def unregister_button(self, button: Button):
        self.button_manager.unregister(button)

    '''Game Objects Attributes'''
    def add_character(self, character: AbstractCharacter):
        self.characters.append(character)
        spawn_button = SpawnButton(
            character=character,
            pixel_pos=(100, (250*(len(self.characters)-1)) + 100)
        )
        self.surfaces.add_to_layer(self.surfaces.ui, spawn_button)
        self.register_button(spawn_button)

    def add_building(self, building):
        self.buildings.append(building)

    def remove_building(self, building):
        if building in self.buildings:
            del self.buildings[building]

    def add_enemy_characters(self, character: AbstractCharacter):
        self.enemy_characters.append(character)

    def remove_enemy_character(self, character: AbstractCharacter):
        if character in self.enemy_characters:
            del self.enemy_buildings[character]

    def add_enemy_buildings(self, building):
        self.enemy_buildings.append(building)

    def remove_enemy_building(self, building):
        if building in self.enemy_buildings:
            del self.enemy_buildings[building]

    '''Action State'''
    def find_interactable_obj(self, mouse_pos: MouseInput) -> Clickable:
        for obj in self.button_manager.buttons.keys():
            if obj.rect.collidepoint(mouse_pos):
                return obj
            
        return self._get_tile_from_pixel(mouse_pos)
    
    def _get_tile_from_pixel(self, pos):
        q, r, s = self.layout.pixel_to_hex_coord(pos)
        try:
            return self.tiles[(q,r)]
        except KeyError:
            return None

    def set_state(self, state: ActionState):
        self.action_state.on_exit()
        self.action_state = state(self)
        self.action_state.on_enter()

    def input(self, mouse_input: MouseInput):
        next_state = self.action_state.input(mouse_input)
        if next_state:
            self.set_state(next_state)

    def update(self, mouse_pos: Tuple[int, int]):
        self.action_state.update(mouse_pos)
                








    

    

    

    



    




