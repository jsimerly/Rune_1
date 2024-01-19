from __future__ import annotations
from typing import TYPE_CHECKING
from mouse_inputs import MouseInput
from in_game.client_state import InGameState
from drafting.client_state import DraftingState
from home_screen.client_state import HomeScreenState
from client_state_proto import ClientState


if TYPE_CHECKING:
    import pygame as pg


class ClientStateManager:
    def __init__(self) -> None:
        self.current_state: ClientState = HomeScreenState()

    def start_draft(self):
        data = self.current_state.on_exit()
        self.current_state = DraftingState(**data)
        self.current_state.on_enter()

    def start_game(self):
        data = self.current_state.on_exit()
        self.current_state = InGameState(**data)
        self.current_state.on_enter()

    def end_game(self):
        data = self.current_state.on_exit()
        self.current_state = HomeScreenState(**data)
        self.current_state.on_enter()

    def input(self, mouse_input: MouseInput):
        if self.current_state:
            self.current_state.input(mouse_input)

        

