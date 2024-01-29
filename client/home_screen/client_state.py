from __future__ import annotations
from client_state_proto import ClientState
from typing import Protocol, Dict, TYPE_CHECKING, List, Callable
from .gui.buttons import StartButton, ExitButton, EnterButton
from mouse_inputs import Click, DragEnd
import pygame as pg
from settings import SCREEN_HEIGHT, SCREEN_WIDTH, BGCOLOR
from api.client_socket import TCPClient
from home_screen.gui.inputs import TextInput
from user.user import User
import asyncio
import websockets

if TYPE_CHECKING:
    from mouse_inputs import MouseInput
    from client.key_inputs import KeyInput
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
        self.user_name_input = TextInput(header='Username')
        self.enter_button = EnterButton(on_click=self.enter_clicked)
        self.buttons.append(self.enter_button)
        self.inputs: List[TextInput] = [self.user_name_input]
        self.selected_input: TextInput = None
       

        self.socket = TCPClient()
    
        self.user = {
            'username': '',
            'is_logged_in': False,
        }
        self.is_waiting_for_game = False
        self.game_found = False

    def render(self, display: pg.Surface):
        display.fill(BGCOLOR)
        logo_center = (SCREEN_WIDTH//2 - 210, 100)
        display.blit(self.logo, logo_center)

        if self.user['is_logged_in']:
            for button in self.buttons:
                button.draw(display)

            if self.is_waiting_for_game:
                self.draw_waiting(display)

            if self.game_found:
                self.draw_game_found(display)
                
        else:
            self.user_name_input.draw(display)
            self.enter_button.draw(display)

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

    def draw_game_found(self, display: pg.Surface):
        text = 'Match Found'
        text_surface = self.font.render(text, True, (255, 255, 255))
        text_position = (775, 620)
        display.blit(text_surface, text_position)

    def mouse_input(self, input: MouseInput):
        if isinstance(input, Click) or isinstance(input, DragEnd):
            self.check_button_for_collision(input.pixel)
            self.check_input_for_collision(input.pixel)

    def key_inputs(self, key_inputs: List[KeyInput]):
        if self.selected_input:
            for key in key_inputs:
                self.selected_input.input(key)

    def check_button_for_collision(self, pixel_pos):
        for button in self.buttons:
            if button.rect.collidepoint(pixel_pos):
                button.on_click()

    def check_input_for_collision(self, pixel_pos):
        for input in self.inputs:
            if input.rect.collidepoint(pixel_pos):
                input.select()
                self.selected_input = input
            else:
                input.unselect()
                if self.selected_input == input:
                    self.selected_input = None

    def enter_clicked(self):
        if self.user_name_input.text != '':
            self.user['username'] = self.user_name_input.text
            self.user['is_logged_in'] = True
            self.buttons.remove(self.enter_button)
            self.socket.login(self.user['username'])

    def start_clicked(self):
        self.is_waiting_for_game = True
        self.start_button.text = 'Cancel'
        self.start_button.on_click = self.cancel_clicked
        
        message = {'username':self.user['username']}
        user = User(username=self.user['username'])
        self.socket.send_message(
            type='lfg',
            user=user,
            serialized_message=message
        )

    ''' Networking '''
        
    def server_input(self, message):
        if message['type'] == 'game_found':
            self.game_found = True
            
    def cancel_clicked(self):
        self.is_waiting_for_game = False
        self.start_button.text = 'Start a Game'
        self.start_button.on_click = self.start_clicked

    def exit_clicked(self):
        self.socket.loop.run_until_complete(self.socket.close_connection())
        pg.quit()

    def on_exit(self) -> Dict:
        self.buttons = []
        self.user_name_input = None

        



