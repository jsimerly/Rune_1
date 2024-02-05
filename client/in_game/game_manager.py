from __future__ import annotations
from ...zclient.ui.buttons.button import ButtonManager, Button
from ...zclient.clickable_obj import Clickable, Draggable, ContinueAction
from typing import List, Dict, Callable, TYPE_CHECKING, Optional, Tuple
from client.in_game.zaction_state import IdleState, ActionState, MouseInput, ActionContext
import pygame as pg
from zclient.ui.buttons.button import ButtonManager
from zclient.ui.buttons.spawn_button import SpawnButton
from objective.runes.rune.rune import Rune
from zclient.ui.buttons.end_turn_button import EndTurnButton
from client.in_game.surfaces import GameSurfaces
if TYPE_CHECKING:
    from map.loadouts.map_layout import MapLayout
    from character.abs_character import AbstractCharacter
    from map.game_tile import GameTile
    from team.team import Team
    from building.abs_building import AbstractBuilding


class GameManager:
    '''
        This is the client side game manager that will hold the state of all objects and manage clicks within the game board and UI. 
    '''
    def __init__(self, 
        map: MapLayout, 
        team: Team,
        team_characters: List[AbstractCharacter],
        enemy_characters: List[AbstractCharacter],
    ):
        self.button_manager = ButtonManager()
        self.surfaces = GameSurfaces()
        self.layout = map.layout

        self.team: Team = team
        self.characters: List[AbstractCharacter] = []
        self.buildings = []
        self.enemy_characters: List[AbstractCharacter] = []
        self.enemy_buildings = []

        self.leveling_stones: List[Rune] = []
        self.leveling_shards = []
        self.altars = []

        self.action_context = ActionContext()
        self.action_state = IdleState(self)
        self.end_turn_callback = None #will inject this on TurnManager instantiation
        self.turn_ended = False

        self.tiles: Dict[Tuple[int,int], GameTile] = map.generate_map()
        for tile in self.tiles.values():
            tile.set_tile_map(self.tiles)
            self.surfaces.add_to_layer(self.surfaces.standard_tiles, tile)

            if tile.building:
                self.surfaces.add_to_layer(self.surfaces.buildings, tile.building)
                if tile.building.team_id == team.team_id:
                    team.add_building(tile.building)   
                    self.buildings.append(tile.building)
                else:
                    self.enemy_buildings.append(tile.building)

            if tile.objective:
                self.surfaces.add_to_layer(self.surfaces.objectives, tile.objective)
                if isinstance(tile.objective, Rune):
                    self.leveling_stones.append(tile.objective)

        for character in team_characters:
            self.add_character(character)

        self.enemy_characters = enemy_characters

        end_button = EndTurnButton() 
        self.register_button(end_button)
        self.surfaces.add_to_layer(self.surfaces.ui, end_button)

    '''Turn'''
    def end_turn(self):
        self.turn_ended = True  
        self.end_turn_callback(
            
        ) #add all the data in json that is needed to handle moves

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

        self.team.add_character(character)
        character.set_team(self.team)

    def add_building(self, building: AbstractBuilding):
        self.buildings.append(building)
        self.team.add_building(building)

    def remove_building(self, building):
        if building in self.buildings:
            del self.buildings[building]
            self.team.remove_building(building)

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
                








    

    

    

    



    




