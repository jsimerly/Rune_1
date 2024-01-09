from __future__ import annotations
from hex import Hex, Layout
from typing import Callable, Optional, List, TYPE_CHECKING
from settings import LIGHT_GREY
import pygame as pg
from game.clickable_obj import AbstractClickableObject
from game.game_phase import GamePhase
from components.map_interaction import MapInteractionComponent
from .click_manager import ClickManager
import time
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
        self.is_selected = False
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

        self.character: AbstractCharacter = None
        self.click_manager = ClickManager(self)

    def set_game_phase(self, game_phase_manager: GamePhaseManager):
        self.game_manager = game_phase_manager
    
    def draw(self, border_color=LIGHT_GREY, border_thickness=1):
        point = self.layout.hex_to_pixel(self)
        verticies = self.layout.get_hex_verticies(point)
        pg.draw.polygon(self.screen, self.color, verticies)

        #not using draw border so we don't hvae to recalculate the vertices and avoid DIing the info into draw border for reusablility.
        outline_size = 4 if self.is_selected else border_thickness
        outline_color = (220,220,220) if self.is_selected else border_color
        pg.draw.polygon(self.screen, outline_color, verticies, outline_size)

        if self.coords_on:
            pg.font.init()
            font = pg.font.SysFont('Arial', 12)
            coord_text = f'{self.q}, {self.r}'
            text_surface = font.render(coord_text, True, (255, 255, 255))
            text_pos = (point[0] - text_surface.get_width() // 2, point[1] - text_surface.get_height() // 2)

            self.screen.blit(text_surface, text_pos)  

    def draw_border(self, border_color=LIGHT_GREY, border_thickness=1):
        point = self.layout.hex_to_pixel(self)
        verticies = self.layout.get_hex_verticies(point)

        outline_color = (220,220,220) if self.is_selected else border_color
        pg.draw.polygon(self.screen, outline_color, verticies, border_thickness)

    def reset_border(self):
        point = self.layout.hex_to_pixel(self)
        inner_verticies = self.layout.get_hex_verticies(point)
        pg.draw.polygon(self.screen, self.color, inner_verticies, 4) #4 is the max thickness we'll have as a border
        self.draw_border()

    def get_center_pixel(self) -> (int, int):  
        return self.layout.hex_to_pixel(self)

    def register_character(self, character: AbstractCharacter):
        self.character = character
        self.character.current_tile = self
        self.character.spawn_to_pixel_pos(self)

    def unregister_character(self):
        self.character = None

    def on_click(self) -> Callable:
        return self.click_manager.on_click()

    def select(self):
        self.is_selected = True
        self.draw_border(border_thickness=3)

    def deselect(self):
        self.is_selected = False
        self.reset_border()

    def redraw_neighbors(self):
        neighbors = self.get_all_neighbor_tiles()
        for tile in neighbors:
            tile.draw()
    
    def redraw_neighbors_borders(self):
        neighbors = self.get_all_neighbor_tiles()
        for tile in neighbors:
            tile.reset_border()

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

