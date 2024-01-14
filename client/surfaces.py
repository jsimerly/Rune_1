from .singleton import Singleton
import pygame as pg
from typing import TYPE_CHECKING, List, Any, Set
if TYPE_CHECKING:
    from map.game_tile import GameTile
    from character.abs_character import AbstractCharacter
    from components.movement import MovementQueue
    from ui.ui_object import UIObject

class GameSurfaces(metaclass=Singleton):
    def __init__(self, screen: pg.Surface) -> None:
        self.screen = screen
        self.standard_tiles: Set[GameTile] = set()
        self.border_tiles: Set[GameTile] = set()
        self.selected_tiles: Set[GameTile] = set()
        self.buildings: Set[Any] = None
        self.movement: Set[MovementQueue] = set()
        self.characters: Set[AbstractCharacter] = set() #include movement and abilities
        self.abilities: Set[Any] = None 
        self.ui: Set[UIObject] = set() #Any really is anything that has a draw method

    def draw(self):
        self.draw_layer(self.standard_tiles)
        self.draw_layer(self.border_tiles)
        self.draw_layer(self.selected_tiles)
        #building
        self.draw_layer(self.movement)
        self.draw_layer(self.characters)
        #ability
        self.draw_layer(self.ui)
        
    def draw_layer(self, layer):
        for obj in layer:
            obj.draw(self.screen)

    def add_to_layer(self, layer: Set, obj):
        layer.add(obj)

    def remove_from_layer(self, layer: Set, obj):
        try:
            layer.remove(obj)
        except KeyError:
            ...
    

    

