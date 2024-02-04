from __future__ import annotations
from typing import TYPE_CHECKING
import pygame as pg
from settings import *

if TYPE_CHECKING:
    from in_game.client_state import InGameState
    from map.game_tile import GameTile

class GameUI:
    def __init__(self, game_state: InGameState) -> None:
        self.state = game_state
        self.coord_on = False

    def draw_tiles(self, display: pg.Surface):
        for tile in self.state.map.tiles.values():
            tile.draw(display)

    def draw_buildings(self, display: pg.Surface):
        for tile in self.state.map.tiles.values():
            if tile.building:
                tile.building.draw(display)

    def draw_objectives(self, display: pg.Surface):
        for tile in self.state.map.tiles.values():
            if tile.objective:
                tile.objective.draw(display)


    def render(self, display: pg.Surface):
        display.fill(BGCOLOR)
        self.draw_tiles(display)
        self.draw_buildings(display)
        self.draw_objectives(display)