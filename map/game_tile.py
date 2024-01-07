from __future__ import annotations
from hex import Hex, Layout
from typing import Callable, Optional, List, TYPE_CHECKING
from settings import LIGHT_GREY
import pygame as pg
from game.clickable_obj import AbstractClickableObject

if TYPE_CHECKING:
    from character.abs_character import AbstractCharacter
    from game_map import GameMap

pg.font.init()

class GameTile(Hex, AbstractClickableObject):
    def __init__(self, 
        q:int, r:int,
        layout: Layout,
        screen,
        game_map: GameMap,
        surface_color: (int, int, int),
    ):
        super().__init__(q, r)
        self.layout = layout
        self.screen = screen
        self.game_map = game_map
        self.is_selected = False

        self.coords_on = True
        self.color = surface_color

        self.character: AbstractCharacter = None
    
    def draw(self):
        point = self.layout.hex_to_pixel(self)
        verticies = self.layout.get_hex_verticies(point)
        pg.draw.polygon(self.screen, self.color, verticies)

        outline_size = 4 if self.is_selected else 1
        outline_color = (220,220,220) if self.is_selected else LIGHT_GREY
        pg.draw.polygon(self.screen, outline_color, verticies, outline_size)

        if self.coords_on:
            pg.font.init()
            font = pg.font.SysFont('Arial', 12)
            coord_text = f'{self.q}, {self.r}'
            text_surface = font.render(coord_text, True, (255, 255, 255))
            text_pos = (point[0] - text_surface.get_width() // 2, point[1] - text_surface.get_height() // 2)

            self.screen.blit(text_surface, text_pos)   

    def get_center_pixel(self) -> (int, int):  
        return self.layout.hex_to_pixel(self)

    def register_character(self, character: AbstractCharacter):
        self.character = character
        self.character.spawn_to_pixel_pos(self.get_center_pixel())

    def unregister_character(self):
        self.character = None

    def on_click(self) -> Callable:
        self.select()
        return self.next_click
    
    def next_click(self, passed_obj: AbstractClickableObject) -> Optional[Callable]:
        self.deselect()
        self.deselect_neighbors()
        next_function = passed_obj.on_click()
        return next_function

    def select(self):
        self.is_selected = True
        self.draw()

    def deselect(self):
        self.is_selected = False
        self.draw()

    def deselect_neighbors(self):
        neighbors = self.get_all_neighors()
        for tile in neighbors:
            axial_coord = (tile.q, tile.r)
            tile = self.game_map.tiles[axial_coord]
            tile.draw()
    
    

