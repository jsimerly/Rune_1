from abc import ABC, abstractmethod
import pygame as pg


class UIObject(ABC):
    @abstractmethod
    def draw(self, screen: pg.Surface):
        ...