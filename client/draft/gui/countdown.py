from ui_objects.abs_ui_object import UIObject
from utils import Timer
import pygame as pg

class Countdown(UIObject):
    def __init__(self, timer:Timer, pos: (int, int)) -> None:
        self.timer=timer
        pg.font.init()
        self.pos = pos
        self.font = pg.font.SysFont(None, 60)

    def draw(self, display: pg.Surface):
        time_left_str = str(self.timer.time_left) + 's'
        text_surface = self.font.render(time_left_str, True, (255, 255, 255))
        display.blit(text_surface, self.pos)