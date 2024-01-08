from __future__ import annotations
from hex import Hex, Layout
from typing import Callable, Optional, List, TYPE_CHECKING
from settings import LIGHT_GREY
import pygame as pg
from game.clickable_obj import AbstractClickableObject
from game.game_phase import GamePhase
from components.map_interaction import MapInteractionComponent

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

        self.coords_on = True
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
        self.prev_func_cache = None

    def set_game_phase(self, game_phase_manager: GamePhaseManager):
        self.game_manager_manager = game_phase_manager
    
    def draw(self, border_color=LIGHT_GREY, border_thickness=1):
        point = self.layout.hex_to_pixel(self)
        verticies = self.layout.get_hex_verticies(point)
        pg.draw.polygon(self.screen, self.color, verticies)

        outline_size = 4 if self.is_selected else border_thickness
        outline_color = (220,220,220) if self.is_selected else border_color
        pg.draw.polygon(self.screen, outline_color, verticies, outline_size)

        if self.character:
            self.character.sprite.draw()

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
        self.character.current_tile = self
        self.character.spawn_to_pixel_pos(self.get_center_pixel())

    def unregister_character(self):
        self.character = None

    def on_click(self) -> Callable:
        current_phase = self.game_manager_manager.current_phase
        if self.character and current_phase == GamePhase.MOVE_QUEUEING:
            movement_options = self.character.movement.find_possible_tiles()
            for tile in movement_options:
                tile.draw(border_color=(200, 200, 200), border_thickness=3)
            
            self.prev_func_cache = movement_options
            return self.handle_click_movement
        
        self.select()
        return self.next_click

    def handle_click_movement(self, passed_object):
        #clear the selection path
        self.game_map.redraw_tiles(self.prev_func_cache)

        if isinstance(passed_object, type(self)):
            if passed_object in self.prev_func_cache:
                movement_path = self.character.movement.astar(passed_object)
                self.game_map.draw_movement_path(movement_path)
                
            else:
                print('Cannot move there')

        self.prev_func_cache = None
        return None
    
    
    def next_click(self, passed_obj: AbstractClickableObject) -> Optional[Callable]:
        self.deselect()
        self.redraw_neighbors()
        next_function = passed_obj.on_click()
        return next_function

    def select(self):
        self.is_selected = True
        self.draw()

    def deselect(self):
        self.is_selected = False
        self.draw()

    def redraw_neighbors(self):
        neighbors = self.get_all_neighbor_tiles()
        for tile in neighbors:
            tile.draw()

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

