from __future__ import annotations
from client_state_proto import ClientState
from typing import Protocol, Dict, TYPE_CHECKING, List
from .gui.buttons import StartButton, ExitButton
from mouse_inputs import Click, DragEnd
from settings import BGCOLOR
import pygame as pg
from settings import SCREEN_HEIGHT, SCREEN_WIDTH
from client_socket import TCPClient

if TYPE_CHECKING:
    from mouse_inputs import MouseInput
    from gui.buttons import TextButton

class HomeScreenState(ClientState):
    def __init__(self) -> None:
        pg.font.init()
        self.font = pg.font.SysFont(None, 36)
        logo_image = pg.image.load('home_screen/gui/rune_logo.webp')
        loading_image = pg.image.load('home_screen/gui/loading_spinner.webp')
        self.logo = pg.transform.scale(logo_image, (400, 400))
        self.loading_logo = pg.transform.scale(loading_image, (50, 50))
        self.logo_angle = 0
        self.start_button = StartButton(on_click=self.start_clicked)
        self.exit_button = ExitButton(on_click=self.exit_clicked)
        self.buttons: List[TextButton] = [self.start_button, self.exit_button]
        self.socket = TCPClient()

        self.is_waiting_for_game = False

    def render(self, display: pg.Surface):
        for button in self.buttons:
            button.draw(display)
        logo_center = (SCREEN_WIDTH//2 - 210, 100)
        display.blit(self.logo, logo_center)

        if self.is_waiting_for_game:
            self.draw_waiting(display)
        else:
            display.fill(BGCOLOR, pg.Rect(700, 600, 500, 60))

    def draw_waiting(self, display: pg.Surface):
        position = (700,600)
        self.logo_angle += 1
        rotated_icon = pg.transform.rotate(self.loading_logo, self.logo_angle)
        new_rect = rotated_icon.get_rect()
        new_rect.topleft = position[0], position[1]
        display.fill(BGCOLOR, new_rect)
        display.blit(rotated_icon, position)

        text = 'Waiting for another player...'
        text_surface = self.font.render(text, True, (255, 255, 255))
        text_position = (775, 620)
        display.blit(text_surface, text_position)

    
    def input(self, input: MouseInput):
        if isinstance(input, Click) or isinstance(input, DragEnd):
            self.check_button_for_collision(input.pixel)

    def check_button_for_collision(self, pixel_pos):
        for button in self.buttons:
            if button.rect.collidepoint(pixel_pos):
                button.on_click()

    def start_clicked(self):
        self.is_waiting_for_game = True
        self.start_button.text = 'Cancel'
        self.start_button.on_click = self.cancel_clicked
        start_data = {'key': 'poop', 'number':420}
        self.socket.create_task(
            self.socket.send_data(start_data)
        )

    def cancel_clicked(self):
        self.is_waiting_for_game = False
        self.start_button.text = 'Start a Game'
        self.start_button.on_click = self.start_clicked

    def exit_clicked(self):
        pg.quit()



