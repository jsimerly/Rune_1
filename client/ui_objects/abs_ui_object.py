
from abc import ABC, abstractmethod
import pygame as pg

class UIObject(ABC):
    @abstractmethod
    def draw(self, screen: pg.Surface):
        ...


class AbsButton(ABC):
    def __init__(self, rect: pg.Rect) -> None:
        self.rect = rect

    @abstractmethod
    def draw(self, screen: pg.Surface):
        ...

    @abstractmethod
    def on_click(self):
        ...