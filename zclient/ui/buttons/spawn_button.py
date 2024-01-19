from .button import Button
from character.abs_character import AbstractCharacter
import pygame as pg
from typing import Tuple
from enum import Enum
from settings import BGCOLOR

class State(Enum):
    UNSELECTED = 1
    SELECTED = 2
    DISABLED = 3

    ...
class SpawnButton(Button):
    def __init__(self, character: AbstractCharacter, pixel_pos: Tuple[int,int]):
        self.character = character

        self.states = State
        self.state = State.UNSELECTED

        self.selected_image = pg.transform.scale(self.character.sprite.standard_image.copy() , (200,200))
        self.image = pg.transform.scale(self.character.sprite.standard_image.copy() , (150,150))
        self.disabled_image = self.image.copy()
        self.disabled_image.set_alpha(100)

        self.rect = self.image.get_rect(center=pixel_pos)
        self.selected_rect = self.selected_image.get_rect(center=pixel_pos)

    def on_click(self):
        if self.state == self.states.DISABLED:
            print("That character has already spawned.")
            return 
        
        if self.state == self.states.UNSELECTED:
            self.set_state(self.states.SELECTED)
        else:
            self.set_state(self.states.UNSELECTED)

    def set_state(self, state):
        self.state = state

    def select(self):
        self.set_state(self.states.SELECTED)

    def deselect(self):
        self.set_state(self.states.UNSELECTED)

    def disable(self):
        self.set_state(self.states.DISABLED) 

    def draw(self, screen: pg.Surface):
        image_map = {
            self.states.UNSELECTED: self.image,
            self.states.SELECTED: self.selected_image,
            self.states.DISABLED: self.disabled_image,
        }

        image = image_map[self.state]
        if self.state == self.states.SELECTED:
            screen.fill(BGCOLOR, self.rect)
            screen.blit(image, self.selected_rect)
        else:
            screen.fill(BGCOLOR, self.selected_rect)
            screen.blit(image, self.rect)
