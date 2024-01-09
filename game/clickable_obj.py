from abc import ABC, abstractmethod
from typing import Callable
import pygame as pg

class AbstractClickableObject(ABC):
    @abstractmethod
    def on_click(self) -> Callable or None:
        """Method to be executed on click."""
        pass

class ClickableRectObj(AbstractClickableObject):
    def __init__(self) -> None:
        self._rect = None
        self.post_init_check()

    def post_init_check(self):
        if not isinstance(self.rect, pg.Rect):
            raise ValueError(f"{self.__class__.__name__} must initialize self.rect with a pygame.Rect")

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
        # Implementation for on_click method
        pass


class AbstactDraggableObj(ABC):
    @abstractmethod
    def on_drag_start(self):
        pass

    @abstractmethod
    def on_drag_update(self):
        pass

    @abstractmethod
    def on_drag_finish(self):
        pass


