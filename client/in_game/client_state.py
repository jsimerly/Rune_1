from __future__ import annotations
from mouse_inputs import MouseInput
from client_state_proto import ClientState
from typing import Protocol, Dict, TYPE_CHECKING
from in_game.map.map import GameMap
from settings import BGCOLOR
from in_game.map.loadouts.map_1 import map_1
from in_game.event_bus import EventBus
from .ecs.ecs_manager import ECSManager
from in_game.action_state import ActionStateManager

if TYPE_CHECKING:
    from mouse_inputs import MouseInput
    import pygame as pg


class InGameState(ClientState):
    def __init__(self, event_bus: EventBus, action_state: ActionStateManager, ecs_manager: ECSManager, map: GameMap) -> None:
        self.event_bus = event_bus
        self.action_state = action_state,
        self.ecs_manager = ecs_manager
        self.map = map

    def mouse_input(self, mouse_input: MouseInput):
        self.event_bus.publish('mouse_input', mouse_input=mouse_input)

    def server_input(self, message: Dict):
        ...

    def render(self, display: pg.Surface):
        display.fill(BGCOLOR)
        self.ecs_manager.render(display)
