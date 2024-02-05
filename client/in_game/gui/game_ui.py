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

    def render(self, display: pg.Surface):
        ...