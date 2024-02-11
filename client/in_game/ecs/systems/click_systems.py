from __future__ import annotations
from in_game.event_bus import EventBus
from in_game.ecs.systems.system_base import System
from in_game.action_state import ActionStateManager
from in_game.ecs.components.occupancy_component import OccupancyComponent
from in_game.entities.buildings.building_base import Building
from in_game.entities.objectives.objective_base import Objective
from in_game.entities.characters.character_base import Character
from in_game.entities.movement_ghost.movement_ghost import MovementGhost
from in_game.ecs.components.screen_position_component import ScreenPositionComponent
from in_game.ecs.components.ui_components import RectUIComponent
from mouse_inputs import MouseInput, Click, DragStart, Dragging, DragEnd
import pygame as pg
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from map.tile import GameTile
    from map.map import GameMap

    from in_game.entities.ui_objects.ui_object_base import ButtonObject

class ClickSystem(System):
    def __init__(self, event_bus: EventBus, action_state: ActionStateManager, game_map: GameMap) -> None:
        super().__init__(event_bus)
        self.action_state = action_state
        self.event_bus = event_bus
        self.game_map = game_map
        self.ui_buttons: set[ButtonObject] = set()
        self.event_bus.subscribe('mouse_input', self.handle_mouse_input)
        self.event_bus.subscribe('tile_clicked_outside_of_move_range', self.outside_of_move_range)

    def add_ui_button(self, button: ButtonObject):
        self.ui_buttons.add(button)

    def remove_ui_button(self, button: ButtonObject):
        self.ui_buttons.remove(button)

    def handle_selected_clicked(self, tile: GameTile):
        self.event_bus.publish('tile_selected', tile=tile)
        occupancy_component: OccupancyComponent = tile.get_component(OccupancyComponent)
 
        for occupant in occupancy_component.occupants:
            if isinstance(occupant, Character):
                self.event_bus.publish('character_selected', character=occupant)   
                break         

        else:
            for occupant in occupancy_component.occupants:
                if isinstance(occupant, MovementGhost):
                    self.event_bus.publish('ghost_selected', ghost=occupant)
                    break
                if isinstance(occupant, Building):
                    self.event_bus.publish('building_selected', building=occupant)
                if isinstance(occupant, Objective):
                    self.event_bus.publish('objective_selected', objective=occupant)
    
    def handle_mouse_input(self, mouse_input: MouseInput):
        pixel = mouse_input.pixel
        tile = self.game_map.pixel_to_tile(pixel)

        if self.action_state.is_idle:
            if isinstance(mouse_input, Click) or isinstance(mouse_input, DragEnd):
                found_action = self.check_buttons(pixel)
                if found_action:
                    return 
                
                if tile:
                    self.handle_selected_clicked(tile)
                    return       
                
        if self.action_state.is_spawning:
            found_action = self.check_buttons(pixel)
            if found_action:
                return
            
            if tile:
                self.event_bus.publish('attempt_spawn_to_tile', tile=tile)
            #return errors
            # self.action_state.idle()
        
        if self.action_state.is_character_selected:
            if tile:
                if isinstance(mouse_input, Click):
                    self.event_bus.publish('attempt_move_to_tile', tile=tile)
                    self.handle_selected_clicked(tile)

                elif isinstance(mouse_input, Dragging):
                    self.event_bus.publish('attempt_drag_to_tile', tile=tile)

                elif isinstance(mouse_input, DragEnd):
                    self.event_bus.publish('movement_ended', tile=tile)
                    self.handle_selected_clicked(tile)
                
            else:
                # check for ui for abliities
                self.action_state.idle()
                
    def outside_of_move_range(self, tile: GameTile):
        print('yo')
        self.action_state.idle()
        self.handle_selected_clicked(tile)


    def check_buttons(self, pixel) -> bool:
        for button in self.ui_buttons:
            button_rect: RectUIComponent = button.get_component(RectUIComponent)
            button_position: ScreenPositionComponent = button.get_component(ScreenPositionComponent)

            rect = pg.Rect(button_position.position, button_rect.size)
            if rect.collidepoint(pixel):
                button.on_click()
                return True

