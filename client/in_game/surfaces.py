from ...zclient.singleton import Singleton
import pygame as pg
from typing import TYPE_CHECKING, List, Any, Set
if TYPE_CHECKING:
    from map.game_tile import GameTile
    from character.abs_character import AbstractCharacter
    from components.movement import MovementQueue
    from ui.ui_object import UIObject
    from building.abs_building import AbstractBuilding
    from objective.abs_objective import AbstactObjective

class GameSurfaces(metaclass=Singleton):
    def __init__(self) -> None:
        self.standard_tiles: Set[GameTile] = set()
        self.border_tiles: Set[GameTile] = set()
        self.selected_tiles: Set[GameTile] = set()
        self.buildings: Set[AbstractBuilding] = set()
        self.objectives: Set[AbstactObjective] = set()
        self.movement: Set[MovementQueue] = set()
        self.characters: Set[AbstractCharacter] = set() #include movement and abilities
        self.abilities: Set[Any] = None 
        self.ui: Set[UIObject] = set() #Any really is anything that has a draw method

    def draw(self, screen: pg.Surface):
        self.draw_layer(self.standard_tiles, screen)
        self.draw_layer(self.border_tiles, screen)
        self.draw_layer(self.selected_tiles, screen)
        self.draw_layer(self.buildings, screen)
        self.draw_layer(self.objectives, screen)
        self.draw_layer(self.movement, screen)
        self.draw_layer(self.characters, screen)
        #ability
        self.draw_layer(self.ui)
        
    def draw_layer(self, layer, screen: pg.Surface):
        for obj in layer:
            obj.draw(screen)

    def add_to_layer(self, layer: Set, obj):
        layer.add(obj)

    def remove_from_layer(self, layer: Set, obj):
        try:
            layer.remove(obj)
        except KeyError:
            ...
    

    

