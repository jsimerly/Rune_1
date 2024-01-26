from typing import List
import pygame as pg

class CharacterPreview:
    def __init__(self, position: (int,int), 
            survivability:int, damage:int, utility:int, difficulty:int,
            abilities: List[List]
        ) -> None:
        size = (400, 400)
        self.position = position
        self.survivability = survivability
        self.damage = damage
        self.utility = utility
        self.difficulty = difficulty
        self.ability = abilities

    def draw(self, display: pg.Surface):
        ...

    def draw_info_type(self, display: pg.Surface, pos:(int,int), name: str, value: int):
        size = (200, 50)
        pg.draw.rect()

