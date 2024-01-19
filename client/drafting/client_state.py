from client_state_proto import ClientState
import pygame as pg

class DraftingState(ClientState):
    

    def render(self, display: pg.Surface):
        display.fill(255, 0, 0)
