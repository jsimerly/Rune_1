from __future__ import annotations
from typing import List, Dict, Callable, TYPE_CHECKING, Optional, Tuple
import pygame as pg

if TYPE_CHECKING:
    from map.loadouts.map_layout import MapLayout
    from character.abs_character import AbstractCharacter
    from map.game_tile import GameTile
    from team.team import Team
    from building.abs_building import AbstractBuilding

class GameMap:
    def __init__(self, map_layout: MapLayout) -> None:
        self.tiles: Dict[Tuple[int,int], GameTile] = map_layout.generate_map()

    def draw_tiles(self, display: pg.Surface):
        for tile in self.tiles.values():
            tile.draw(display)

    def draw_vision(self):
        pass