from __future__ import annotations
from objective.abs_objective import AbstactObjective
from components.sprite import SpriteComponent
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from map.game_tile import GameTile
    import pygame as pg


class Rune(AbstactObjective):
    def __init__(self, 
        tile: GameTile, 
        radius: int, 
        power:int, 
        image_path: str,
        spawn_turn: int = 0, 
    ) -> None:
        super().__init__(spawn_turn)
        self.tile: GameTile = tile 
        self.radius = radius
        self.power = power #power is how much level up is given at the center.

        image = self.open_image(image_path)
        self.set_sprite_comp(image)
        self.sprite.move_to_tile(self.tile)
        

    def find_character_in_range(self):
        self.tile

    def on_end_of_turn(self):
        super().on_end_of_turn()
        self.find_character_in_range()

