import pygame as pg
from settings import *
from mouse_inputs import Click, DragStart, Dragging, DragEnd
from client_state_manager import ClientStateManager
from client_socket import TCPClient
import asyncio

class Game:
    def __init__(self) -> None:
        pg.init()

        self.screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pg.SRCALPHA)
        self.screen.fill(BGCOLOR)
        self.clock = pg.time.Clock()
        self.is_running = True

        self.is_dragging = False
        self.mouse_down_pos = None
        self.drag_threshold = 30

        self.state_manager = ClientStateManager() 
        self.socket = TCPClient()

    def get_mouse_action(self, events):
        mouse_pos = pg.mouse.get_pos()
        for event in events:
            if event.type == pg.MOUSEBUTTONDOWN:
                if not self.mouse_down_pos:
                    self.mouse_down_pos = mouse_pos

            if event.type == pg.MOUSEBUTTONUP:
                if self.is_dragging:
                    self.is_dragging = False
                    self.mouse_down_pos = None
                    return DragEnd(mouse_pos)
                return Click(mouse_pos)
            
            if self.mouse_down_pos and not self.is_dragging:
                if self.drag_threshold_reached(mouse_pos):
                    self.is_dragging = True
                    return DragStart(mouse_pos)

            if self.is_dragging:
                return Dragging(mouse_pos)
            
            return None

    def drag_threshold_reached(self, mouse_pos):
            dx = mouse_pos[0] - self.mouse_down_pos[0]
            dy = mouse_pos[1] - self.mouse_down_pos[1]
            distance = (dx**2 + dy**2)**0.5
            return distance > self.drag_threshold
    
    def render(self):
        self.state_manager.current_state.render(self.screen)
        pg.display.flip()

    def game_loop(self):
        events = pg.event.get()
        for event in events:
            if event.type == pg.QUIT:
                self.is_running = False
                return

        mouse_action = self.get_mouse_action(events)
        if mouse_action:
            self.state_manager.current_state.input(mouse_action)
        self.render()
        
        self.socket.run_one()
        
        if self.clock.get_time() > 150:
            print(self.clock.get_time())
        self.clock.tick(FPS)

    
if __name__ == '__main__':
    game = Game()
    while game.is_running:
        game.game_loop()
    pg.quit()
