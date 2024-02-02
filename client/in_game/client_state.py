from __future__ import annotations
from client_state_proto import ClientState
from typing import Protocol, Dict, TYPE_CHECKING
if TYPE_CHECKING:
    from mouse_inputs import MouseInput
    import pygame as pg

class InGameState(ClientState):
    def __init__(self, game_data) -> None:
        ...

    def render(self, display: pg.Surface):
        ...
