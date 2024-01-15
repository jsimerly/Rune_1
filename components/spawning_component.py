from __future__ import annotations
from components.abstact_component import AbstactComponent
from algorithms import hex_reachable
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from map.game_tile import GameTile


class SpawningComponent(AbstactComponent):
    def __init__(self, radius:int, center_tile: GameTile) -> None:
        self.center_tile: GameTile = center_tile
        self.radius = radius

    def update_radius(self, radius:int):
        self.radius = radius

    def update_center_tile(self, tile:GameTile):
        self.center_tile = tile
    
    def find_spawnable(self) -> List[GameTile]:
        options = []
        for q in range(-self.radius, self.radius + 1):
            r1 = max(-self.radius, -q - self.radius)
            r2 = min(self.radius, -q + self.radius) + 1
            for r in range(r1, r2):
                tile_cords = (self.center_tile.q + q, self.center_tile.r + r)
                if tile_cords in self.center_tile.tile_map:
                    tile = self.center_tile.tile_map[tile_cords]
                    if tile.map_interaction.can_end_on:
                        options.append(tile)

        return options