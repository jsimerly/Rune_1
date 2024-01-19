import pygame as pg
from key_inputs import KeyInput
from settings import SCREEN_WIDTH, SCREEN_HEIGHT


class TextInput:
    def __init__(self, header:str) -> None:
        size = (300, 60)
        x, y = (SCREEN_WIDTH - size[0])//2, SCREEN_HEIGHT//2,
        self.rect = pg.Rect(x, y, size[0], size[1])
        self.header = header
        self.is_selected = False
        self.text = ''

        pg.font.init()
        self.font = pg.font.SysFont(None, 36)

    def select(self):
        self.is_selected = True

    def unselect(self):
        self.is_selected = False

    def input(self, key: KeyInput):
        if key.unicode == '\x08':
            self.text = self.text[:-1]
        else:
            self.text += key.unicode

    def draw(self, screen: pg.Surface):
        pg.draw.rect(screen, (255, 255, 255), self.rect)
        if self.is_selected:
            pg.draw.rect(screen, (0,170,255), self.rect, 3)

        text_surface = self.font.render(self.text, True, (0,0,0))
        point = self.rect.center
        text_pos = (point[0] - text_surface.get_width() // 2, point[1] - text_surface.get_height() // 2)
        screen.blit(text_surface, text_pos)