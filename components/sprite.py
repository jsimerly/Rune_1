from .abstact_component import AbstactComponent
import pygame as pg

class SpriteComponent(AbstactComponent):
    NORMAL_SIZE = (60,60)

    def __init__(self, image: pg.image, screen):
        self.is_selected = False
        self.screen = screen
        self.pixel_pos = None
        self.image = pg.transform.scale(image, self.NORMAL_SIZE)

    def get_topleft_pos(self) -> (int, int):
        x, y = self.pixel_pos
        x -= self.NORMAL_SIZE[0] // 2
        y -= self. NORMAL_SIZE[1] // 2
        return ((x,y))

    def spawn_to_pixel(self, pixel):
        self.pixel_pos = pixel
        self.draw()

    def draw(self):
        top_left_pixel = self.get_topleft_pos()
        self.screen.blit(self.image, top_left_pixel)