import pygame as pg


class UsernameUI:
    def __init__(self, username: str, pos: (int,int)) -> None:
        self.username = username
        self.pos = pos
        pg.font.init()
        self.font = pg.font.SysFont(None, 60)

    def draw(self, display: pg.Surface):
        text_surface = self.font.render(self.username, True, (255, 255, 255))
        display.blit(text_surface, self.pos)