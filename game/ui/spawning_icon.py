from __future__ import annotations
from typing import TYPE_CHECKING
import pygame as pg
from settings import BGCOLOR
from game.clickable_obj import ClickableRectObj
from exceptions import PlayerError
from map.game_map import GameTile

if TYPE_CHECKING:
    from character.abs_character import AbstractCharacter

class CharacterSpawningIcon(ClickableRectObj):
    NORMAL_SIZE = (150, 150)
    SELECTED_SIZE = (200, 200)
    NOT_SELECT_ALPHA = 100

    def __init__(self, image, pixel_pos, screen, char_instance):
        self.screen = screen
        self.is_selected = False
        self.is_disabled = False
        self.pos = pixel_pos
        self.char_instance = char_instance

        self.image = pg.transform.scale(image, self.NORMAL_SIZE)
        self.selected_image = pg.transform.scale(image, self.SELECTED_SIZE)
        self.disabled_image = self.image.copy()
        self.disabled_image.set_alpha(self.NOT_SELECT_ALPHA)

        self.rect = self.image.get_rect(center=pixel_pos)
        self.selected_rect= self.selected_image.get_rect(center=pixel_pos)
    
    def draw(self):
        if self.is_disabled:
            self.screen.fill(BGCOLOR, self.selected_rect)
            self.screen.blit(self.disabled_image, self.rect)
            return

        current_image = self.image
        current_rect = self.rect
        if self.is_selected:
            current_image = self.selected_image
            current_rect = self.selected_rect

        self.screen.fill(BGCOLOR, self.selected_rect)
        self.screen.blit(current_image, current_rect.topleft)

    def select(self):
        if self.is_disabled:
            print("You cannot do that right now.")
        self.is_selected = not self.is_selected
        self.draw()
    
    def on_click(self):
        self.select()
        return self.next_click

    def next_click(self, passed_object):
        if isinstance(passed_object, GameTile):
            if passed_object.character:
                print('You cannot place a character on top of another character.')
                self.select()
                return None
            else:
                passed_object.register_character(character=self.char_instance)
                self.disable()
                return None
        
        if self == passed_object:
            self.select()
            return None

    def disable(self):
        self.is_disabled = True
        self.draw()

    def enable(self):
        self.is_disabled = False
        self.draw()

