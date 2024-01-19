from __future__ import annotations
from typing import Protocol, Dict, TYPE_CHECKING
if TYPE_CHECKING:
    from mouse_inputs import MouseInput
    import pygame as pg

class ClientState(Protocol):
    def on_enter(self):
        ...

    def on_exit(self) -> Dict:
        ...

    def input(self, mouse_input: MouseInput):
        ...

    def render(self, display: pg.Surface):
        ...
