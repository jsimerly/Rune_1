from typing import Callable, Dict, Any, List
from abc import ABC, abstractmethod
import pygame as pg
from client.ui.ui_object import UIObject


class Button(UIObject):
    def __init__(self):
        self._rect = None

    @property
    def rect(self):
        return self._rect

    @rect.setter
    def rect(self, value):
        if not isinstance(value, pg.Rect):
            raise ValueError("rect must be a pg.Rect instance")
        self._rect = value

    @abstractmethod
    def on_click(self) -> Callable or None:
        '''Method to be executed on click'''
        ...

    @abstractmethod
    def draw(self):
        ...

class ButtonManager:
    def __init__(self):
        self.buttons: Dict[Button, List[Callable]] = {}
        self.selected_obj = None

    def register(self, button:Button):
        if button in self.buttons:
            self.buttons[button].append(button.on_click)
        else:
            self.buttons[button] = button.on_click

    def unregister(self, button):
        del self.buttons[button]

    def run_event_for(self, button):
        fn = self.buttons[button]
        fn()
