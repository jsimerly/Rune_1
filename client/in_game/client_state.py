from __future__ import annotations
from mouse_inputs import MouseInput
from client_state_proto import ClientState
from typing import Protocol, Dict, TYPE_CHECKING
from in_game.map.map import GameMap
from settings import BGCOLOR
from in_game.map.loadouts.map_1 import map_1
from .gui.game_ui import GameUI
from in_game.event_bus import EventBus
from .ecs.ecs_manager import ECSManager
from in_game.action_state import ActionStateManager

if TYPE_CHECKING:
    from mouse_inputs import MouseInput
    import pygame as pg


class InGameState(ClientState):
    def __init__(self, game_data) -> None:
        self.event_bus = EventBus()
        self.action_state = ActionStateManager(self.event_bus)
        self.ecs_manager = ECSManager(self.event_bus, self.action_state)
        self.map = GameMap(map_loadout=map_1, ecs_manager=self.ecs_manager, event_bus=self.event_bus)

    def mouse_input(self, mouse_input: MouseInput):
        self.event_bus.publish('mouse_event', mouse_input)

    def server_input(self, message: Dict):
        ...

    def render(self, display: pg.Surface):
        display.fill(BGCOLOR)
        self.ecs_manager.render(display)
