from __future__ import annotations
from components.abstact_component import AbstactComponent
from client.algorithms import in_radius_end_on
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
        options = in_radius_end_on(self.center_tile, self.radius)
        return options