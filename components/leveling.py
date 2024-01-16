from components.abstact_component import AbstactComponent
from typing import Tuple
import pygame as pg
from settings import DARK_GREY

pg.font.init()
font = pg.font.SysFont('Arial Bold', 20)

class LevelingComponent(AbstactComponent):
    def __init__(self, level_thresholds=None) -> None:
        self.level = 1
        self.pp = 0
        if level_thresholds is None:
            level_thresholds = [1000, 3000]
        self.level_thresholds = level_thresholds

    def add_pp(self, pp:int):
        if self.level == 3:
            return
        self.pp += pp
        self.check_for_level_up()

    def remove_pp(self, pp: int):
        self.pp -= pp

    def check_for_level_up(self) -> bool:
        if self.level <= len(self.level_thresholds):
            threshold = self.level_thresholds[self.level-1]
            if self.pp >= threshold:
                self.level_up()

    def level_up(self) -> int:
        self.level += 1
        return self.level
    
    def draw(self, screen: pg.Surface, pixel_pos:Tuple[int,int]):
        text_surface = font.render(str(self.level), True, (255, 255, 255))
        screen.blit(text_surface, pixel_pos)
        