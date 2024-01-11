from ui.buttons.button import ButtonManager, Button
from clickable_obj import Clickable, Draggable, ContinueAction
from character.abs_character import AbstractCharacter
from typing import List, Dict, Callable, TYPE_CHECKING, Optional
from client.click_states.action_state import IdleState, ActionState, DragAction, ClickAction
import pygame as pg
from surfaces import Surfaces
from client.ui.buttons.button import ButtonManager
if TYPE_CHECKING:
    from map.loadouts.map_layout import MapLayout


class GameManager:
    '''
        This is the client side game manager that will hold the state of all objects and manage clicks within the game board and UI. 
    '''
    def __init__(self, map: MapLayout, screen: pg.Surface):
        self.button_manager = ButtonManager() #event manager for buttons
        self.surfaces = Surfaces(screen=screen)
        self.layout = map.layout

        self.tiles = map.generate_map(self.surfaces.tile_surface)
        self.characters: List[AbstractCharacter] = []
        self.buildings = []
        self.enemy_characters: List[AbstractCharacter] = []
        self.enemy_buildings = []

        self.leveling_stones = []
        self.leveling_shards = []
        self.altars = []

        self.is_dragging = False
        self.action_state = IdleState()

    '''Register Events'''
    
    def register_button(self, button: Button):
        self.button_manager.register(button)

    def unregister_button(self, button: Button):
        self.button_manager.unregister(button)

    '''Game Objects Attributes'''
    def add_character(self, character: AbstractCharacter):
        self.characters.append(character)

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
    def find_interactable_obj(self, mouse_pos) -> Clickable:
        for obj in self.button_manager.buttons:
            if obj.rect.collidepoint(mouse_pos):
                return obj
            
        return self._get_tile_from_pixel(mouse_pos)
    
    def _get_tile_from_pixel(self, pos):
        q, r, s = self.layout.pixel_to_hex_coord(pos)
        try:
            return self.tiles[(q,r)]
        except KeyError:
            return None
        
    def on_click(self, mouse_pos):
        obj = self.find_interactable_obj(mouse_pos)
        if self.is_dragging:
            self.input(DragAction(obj))
        else:
            self.input(ClickAction(obj))

    def set_state(self, state: ActionState):
        self.action_state = state

    def input(self):
        self.action_state.input()

    def update(self):
        self.action_state.update()
                








    

    

    

    



    




