from __future__ import annotations
from typing import Protocol, Dict, TYPE_CHECKING, List
if TYPE_CHECKING:
    from mouse_inputs import MouseInput
    from key_inputs import KeyInput
    import pygame as pg

class ClientState(Protocol):
    def on_enter(self):
        ...

    def on_exit(self) -> Dict:
        ...

    def mouse_input(self, mouse_input: MouseInput):
        ...

    def key_inputs(self, key_inputs: List[KeyInput]):
        ...

    def render(self, display: pg.Surface):
        ...
