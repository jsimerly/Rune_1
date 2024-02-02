from __future__ import annotations
from client_state_proto import ClientState
from typing import Protocol, Dict, TYPE_CHECKING
from map.map import GameMap
from settings import BGCOLOR
from map.loadouts.map_1 import map_1
if TYPE_CHECKING:
    from mouse_inputs import MouseInput
    import pygame as pg

class InGameState(ClientState):
    def __init__(self, game_data) -> None:
        self.map = GameMap(map_layout=map_1)
        self.team = 0 #team object
        self.opponent = 0 #opponent team

        ...

    def render(self, display: pg.Surface):
        display.fill(BGCOLOR)
        self.map.draw_tiles(display)
        self.map.draw_buildings(display)
        self.map.draw_objectives(display)
