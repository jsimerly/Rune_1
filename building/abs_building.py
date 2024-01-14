from abc import ABC, abstractmethod
from components.sprite import SpriteComponent
import pygame as pg

class AbstractBuilding(ABC):
    
    @property
    @abstractmethod
    def is_passable(self):
        ...

    @property
    @abstractmethod
    def can_pierce(self):
        ...

    @property
    @abstractmethod
    def can_end_on(self):
        ...

    @property
    @abstractmethod
    def blocks_vision(self):
        ...

    @property
    @abstractmethod
    def hides_occupants(self):
        ...

    @property
    @abstractmethod
    def is_slowing(self):
        ...

    @property
    @abstractmethod
    def walkthrough_effects(self):
        ...

    def set_sprite_comp(self, image: pg.Surface):
        self.sprite = SpriteComponent(image)

    def open_image(self, image_path) -> pg.image:
        return pg.image.load(image_path).convert_alpha()

    def draw(self, screen: pg.Surface):
        self.sprite.draw(screen)
        self.sprite.draw_ghost(screen)