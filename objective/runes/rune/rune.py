from __future__ import annotations
from objective.abs_objective import AbstactObjective
from components.sprite import SpriteComponent
from typing import TYPE_CHECKING, List
from algorithms import hex_radius

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
        

    def find_tiles_in_range(self) -> List[GameTile]:
        return hex_radius(self.tile, self.radius)

    def on_end_of_turn(self):
        super().on_end_of_turn()

    def _get_opacity(self, distance):
        opacity_map = {
            0: 70,
            1: 70,
            2: 55,
            3: 40,
            4: 25,
        }
        if distance in opacity_map:
            return opacity_map[distance]
        return 15

    def draw(self, screen: pg.Surface):
        super().draw(screen)
        tiles_in_range = self.find_tiles_in_range()
        for in_range_tile in tiles_in_range:
            distance = in_range_tile.distance_to(self.tile)
            opacity = self._get_opacity(distance)

            in_range_tile.draw_overlay(screen, (0,170,255, opacity))

        #when we die remove the tile cache
        

