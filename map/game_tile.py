from __future__ import annotations
from hex import Hex, Layout
from typing import Callable, Optional, List, TYPE_CHECKING
from settings import LIGHT_GREY
import pygame as pg
from game.clickable_obj import AbstractClickableObject
from game.game_phase import GamePhase
from components.map_interaction import MapInteractionComponent
from .click_manager import ClickManager
from abc import ABC, abstractmethod
from math import radians, cos, sin
from utils import time_it

if TYPE_CHECKING:
    from character.abs_character import AbstractCharacter
    from game_map import GameMap
    from game.brock_purdy import GamePhaseManager

pg.font.init()

class GameTile(Hex, AbstractClickableObject):
    def __init__(self, 
        q:int, r:int,
        layout: Layout,
        screen,
        game_map: GameMap,

        surface_color: (int, int, int),
        is_passable, 
        can_pierce,
        can_end_on, 
        blocks_vision, 
        hides_occupants, 
        is_slowing, 
        walkthrough_effects: List[Callable] = []
    ):
        super().__init__(q, r)
        self.layout = layout
        self.screen = screen
        self.game_map = game_map
        self.game_phase_manager = None

        self.coords_on = False
        self.color = surface_color
        self.map_interaction = MapInteractionComponent(
            is_passable=is_passable,
            can_pierce=can_pierce,
            can_end_on=can_end_on,
            blocks_vision=blocks_vision,
            hides_occupants=hides_occupants,
            is_slowing=is_slowing,
            walkthrough_effects=walkthrough_effects
        )

        self.is_selected = False
        self.is_option = False

        self.character: AbstractCharacter = None
        self.ghost_character: AbstractCharacter = None
        self.click_manager = ClickManager(self)

    ''' Render Registers
        This is used to add and remove things that need to be rerenders on the next cycle. This is handled by the GameMap instance attached to every time.
    '''
    def register_full_render(self):
        self.game_map.render.add_full_tiles([self])

    def register_border_render(self):
        self.game_map.render.add_borders([self])

    def register_selection_render(self):
        self.game_map.render.add_selection(self)

    def register_neighor_full_render(self):
        neighbors = self.get_all_neighbor_tiles()
        for tile in neighbors:
            tile.register_full_render()

    def register_neighor_border_render(self):
        neighbors = self.get_all_neighbor_tiles()
        for tile in neighbors:
            tile.register_border_render()

    def unregister_full_tile(self):
        self.game_map.render.remove_full_tile(self)

    def unregister_border(self):
        self.game_map.render.remove_border(self)

    def unregister_selection(self):
        self.game_map.render.remove_selection(self)

    def set_game_phase(self, game_phase_manager: GamePhaseManager):
        self.game_manager = game_phase_manager
    
    ''' Drawing
        This section is for actually rendering the tile and it's objects on onto the canvas.
    '''
    def draw(self):
        self.draw_background()
        self.draw_border()
        if self.character:
            self.draw_character()
        if self.ghost_character:
            self.draw_ghost()

        if self.coords_on:
            point = self.center_pixel
            pg.font.init()
            font = pg.font.SysFont('Arial', 12)
            coord_text = f'{self.q}, {self.r}'
            text_surface = font.render(coord_text, True, (255, 255, 255))
            text_pos = (point[0] - text_surface.get_width() // 2, point[1] - text_surface.get_height() // 2)

            self.screen.blit(text_surface, text_pos)  
    
    def draw_background(self):
        verticies = self.verticies
        pg.draw.polygon(self.screen, self.color, verticies)

    def draw_border(self):
        outline_size = 1
        outline_color = LIGHT_GREY
        if self.is_option:
            outline_size = 3
            outline_color = (200, 200, 200)

        if self.is_selected:
            outline_size = 4
            outline_color = (220, 220, 220)

        pg.draw.polygon(self.screen, self.color, self.verticies, 4) #used to reset previous border
        pg.draw.polygon(self.screen, outline_color, self.verticies ,outline_size)

    def fill_outline(self):
        pass
        
    def draw_character(self):
        if self.character:
            pixel_pos = self.center_pixel
            self.character.sprite.draw(pixel_pos)

    def draw_ghost(self):
        if self.ghost_character:
            pixel_pos = self.center_pixel
            self.ghost_character.sprite.draw_ghost(pixel_pos)

    #consider pre processing this if it's taking too much time
    def inner_verticies(self):
        center = self.center_pixel
        verticies = []
        for corner in range(6):
            offset = self.offset_inner_vert(corner)
            x, y = (center[0] + offset[0], center[1] + offset[1])
            x = int(round(x, 0))
            y = int(round(y, 0))
            verticies.append((x, y))

        return verticies

    def offset_inner_vert(self, corner:int):
        angle = 60 * corner + 60
        rad = radians(angle)
        y = (self.layout.size[0] - 1) * cos(rad)
        x = (self.layout.size[1] - 1) * sin(rad)

        x += self.layout.skew * y
        return (x, y)

    @property  
    def center_pixel(self) -> (int, int):  
        return self.layout.hex_to_pixel(self)
    
    @property
    def verticies(self) -> (int, int):
        center = self.layout.hex_to_pixel(self)
        return self.layout.get_hex_verticies(center)
    
    ''' Character
        This section is used to manager characters.
    '''

    def add_character(self, character: AbstractCharacter):
        self.character = character
        self.character.current_tile = self
        self.register_full_render()

    def remove_character(self):
        self.character = None
        self.register_full_render()

    def on_click(self) -> Callable:
        return self.click_manager.on_click()
    
    #helper function for click_manager
    def is_gametile_type(self, obj) -> bool:
        return isinstance(obj, GameTile)

    '''Property Methods
        Use these to manage the state of the tiles. This helps with both gameplay and rendering.
    '''
    def select(self):
        self.is_selected = True
        self.register_selection_render()

    def deselect(self):
        self.is_selected = False
        self.unregister_selection()
        self.register_selection_render()

    def set_option(self):
        self.is_option = True
        self.register_border_render()

    def remove_option(self):
        self.is_option = False
        self.register_border_render()
    
    def get_neighbor_tile(self, i) -> GameTile:
        hex = self.neighbor(i)
        if hex.axial in self.game_map.tiles:
            return self.game_map[hex.axial]
        return None
    
    def get_all_neighbor_tiles(self) -> List[GameTile]:
        neighbor_hex = self.get_all_neighors()
        tiles = []
        for hex in neighbor_hex:
            if hex.axial in self.game_map.tiles:
                tiles.append(self.game_map.tiles[hex.axial])
        return tiles
    
    def __repr__(self) -> str:
        return f'{self.__class__.__name__} Object: {self.q}, {self.r}'


