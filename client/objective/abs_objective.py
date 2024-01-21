from __future__ import annotations
from abc import ABC, abstractmethod
from components.sprite import SpriteComponent
from components.map_interaction import MapInteractionComponent
from typing import TYPE_CHECKING
import pygame as pg

if TYPE_CHECKING:
    from map.game_tile import GameTile



class AbstactObjective(ABC):
    def __init__(self, spawn_turn: int = 0) -> None:
        self.spawn_turn = spawn_turn
        self.duration = None
        self.sprite: SpriteComponent
        self.map_interatcion: MapInteractionComponent
        
    @abstractmethod
    def on_end_of_turn(self):
        ...

    def set_sprite_comp(self, image: pg.Surface):
        self.sprite = SpriteComponent(image)

    def set_tile(self, tile: GameTile):
        self.tile = tile

    def open_image(self, image_path) -> pg.image:
        return pg.image.load(image_path).convert_alpha()
    
    def draw(self, screen: pg.Surface):
        self.sprite.draw(screen)

    

    