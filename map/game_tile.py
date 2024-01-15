from __future__ import annotations
from hex import Hex, Layout
from typing import Callable, Optional, List, TYPE_CHECKING, Dict, Tuple
from settings import LIGHT_GREY
import pygame as pg
from components.map_interaction import MapInteractionComponent
from abc import ABC, abstractmethod
from math import radians, cos, sin
from utils import time_it
from client.surfaces import GameSurfaces

if TYPE_CHECKING:
    from character.abs_character import AbstractCharacter
    from building.abs_building import AbstractBuilding


pg.font.init()

class GameTile(Hex):
    def __init__(self, 
        q:int, r:int,
        layout: Layout,
        #add border and selection surface

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
        self.surface = GameSurfaces()

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
        self.tile_map: Dict[Tuple[int,int], GameTile] = None

        self.character: AbstractCharacter = None
        self.ghost_character: AbstractCharacter = None
        self.building: AbstractBuilding = None

    '''Character'''
    def spawn_character(self, character: AbstractCharacter):
        self.character = character
        self.ghost_character = character
        character.spawn_to(self)
        self.resolve_other_map_interactions()

    def character_move_to(self, other_tile: GameTile):
        other_tile.add_character(self.ghost_character)
        if other_tile != self:
            self.remove_character()

    def add_character(self, character: AbstractCharacter):
        self.character = character
        character.current_tile = self
        self.resolve_other_map_interactions()

    def remove_character(self):
        self.character = None
        self.resolve_other_map_interactions()

    '''Buildings'''

    def add_building(self, building: AbstractBuilding):
        self.building = building   
        self.resolve_other_map_interactions()

    def remove_building(self, building: AbstractBuilding):
        self.building = building
        self.resolve_other_map_interactions()
    
    ''' Drawing
        This section is for actually rendering the tile and it's objects on onto the canvas.
    '''
    def draw(self, screen: pg.Surface):
        self.draw_background(screen)
        self.draw_border(screen)

        if self.coords_on:
            coord_text = f'{self.q}, {self.r}'
            self.draw_text(screen, coord_text)
         
    
    def draw_text(self, screen: pg.Surface, text: str):
            point = self.center_pixel
            pg.font.init()
            font = pg.font.SysFont('Arial', 12)
            text_surface = font.render(text, True, (255, 255, 255))
            text_pos = (point[0] - text_surface.get_width() // 2, point[1] - text_surface.get_height() // 2)

            screen.blit(text_surface, text_pos)  
    
    def draw_background(self, screen: pg.Surface):
        verticies = self.verticies        
        pg.draw.polygon(screen, self.color, verticies)

    def draw_border(self, screen:pg.Surface, color=None):
        outline_size = 1
        outline_color = LIGHT_GREY
        if self.is_option:
            outline_size = 2
            outline_color = (200, 200, 200)

        if self.is_selected:
            outline_size = 4
            outline_color = (220, 220, 220)

        if color:
            outline_color = color
 
        pg.draw.polygon(screen, outline_color, self.verticies, outline_size)
        
    def move_to_border_layer(self):
        self.surface.add_to_layer(self.surface.border_tiles, self)
        self.surface.remove_from_layer(self.surface.standard_tiles, self)
        self.surface.remove_from_layer(self.surface.selected_tiles, self)

    def move_to_selection_layer(self):
        self.surface.add_to_layer(self.surface.selected_tiles, self)
        self.surface.remove_from_layer(self.surface.standard_tiles, self)
        self.surface.remove_from_layer(self.surface.border_tiles, self)

    def move_to_standard_layer(self):
        self.surface.add_to_layer(self.surface.standard_tiles, self)
        self.surface.remove_from_layer(self.surface.selected_tiles, self)
        self.surface.remove_from_layer(self.surface.border_tiles, self)

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
    
    ''' Properties '''

    @property  
    def center_pixel(self) -> (int, int):  
        return self.layout.hex_to_pixel(self)
    
    @property
    def verticies(self) -> (int, int):
        center = self.layout.hex_to_pixel(self)
        return self.layout.get_hex_verticies(center)
    
    def set_tile_map(self, tile_map):
        self.tile_map = tile_map

    def resolve_other_map_interactions(self) -> MapInteractionComponent:
        other_mi: Optional[MapInteractionComponent] = None
        if self.character:
            other_mi = self.character.map_interaction
            
        if self.building:
            other_mi = self.building.map_interaction

        is_passable = self.map_interaction.default_is_passable
        can_pierce = self.map_interaction.default_can_pierce
        can_end_on = self.map_interaction.default_can_end_on
        blocks_vision = self.map_interaction.default_blocks_vision
        hides_occupants = self.map_interaction.default_hides_occupants
        is_slowing = self.map_interaction.default_is_slowing

        if other_mi:
            # Dominant value assignment (not is the dominant)
            is_passable = is_passable and other_mi.is_passable # False
            can_pierce = can_pierce and other_mi.can_pierce # False
            can_end_on = can_end_on and other_mi.can_end_on # False
            blocks_vision = blocks_vision or other_mi.blocks_vision # True
            hides_occupants = hides_occupants or other_mi.hides_occupants # True
            is_slowing = self.map_interaction or is_slowing # True

        self.map_interaction.is_passable = is_passable
        self.map_interaction.can_pierce = can_pierce
        self.map_interaction.can_end_on = can_end_on
        self.map_interaction.blocks_vision = blocks_vision
        self.map_interaction.hides_occupants = hides_occupants
        self.map_interaction.is_slowing = is_slowing

        return self.map_interaction



    def select(self): #may need to add logic to selection to handle the rendering
        self.is_selected = True
        self.move_to_selection_layer()

    def deselect(self):
        self.is_selected = False
        self.move_to_standard_layer()

    def set_option(self):
        self.is_option = True
        self.move_to_border_layer()

    def remove_option(self):
        self.is_option = False
        self.move_to_standard_layer()
    
    def get_neighbor_tile(self, i) -> GameTile:
        hex = self.neighbor(i)
        if hex.axial in self.tile_map:
            return self.tile_map[hex.axial]
        return None
    
    def get_all_neighbor_tiles(self) -> List[GameTile]:
        neighbor_hex = self.get_all_neighors()
        tiles = []
        for hex in neighbor_hex:
            if hex.axial in self.tile_map:
                tiles.append(self.tile_map[hex.axial])
        return tiles
    
    def __repr__(self) -> str:
        return f'{self.__class__.__name__} Object: {self.q}, {self.r}'


