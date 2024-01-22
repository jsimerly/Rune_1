from .abs_state import AbstactGameState
from typing import Callable

class InGameState(AbstactGameState):
    def __init__(self, on_complete: Callable) -> None:
        self.on_complete = on_complete

    def on_enter(self):
        return super().on_enter()
    
    def on_exit(self):
        return super().on_exit()
    
    def handle_server_message(self):
        return super().handle_server_message()