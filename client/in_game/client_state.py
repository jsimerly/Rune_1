from __future__ import annotations
from client_state_proto import ClientState
from typing import Protocol, Dict, TYPE_CHECKING
from in_game.map.map import GameMap
from settings import BGCOLOR
from in_game.map.loadouts.map_1 import map_1
from .gui.game_ui import GameUI
from .ecs.ecs_manager import ECSManager

if TYPE_CHECKING:
    from mouse_inputs import MouseInput
    import pygame as pg

class InGameState(ClientState):
    def __init__(self, game_data) -> None:
        self.ecs_manager = ECSManager()
        self.map = GameMap(map_loadout=map_1, ecs_manager=self.ecs_manager)
        self.team = 0 #team object, 
        self.opponent = 0 #opponent team



    def render(self, display: pg.Surface):
        self.ecs_manager.render(display)
