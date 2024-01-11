from singleton import Singleton
import pygame as pg

class Surfaces(metaclass=Singleton):
    def __init__(self, screen: pg.Surface) -> None:
        self.screen = screen
        self.tile_surface = pg.Surface(screen.get_size(), (0,0))
        self.border_surface = pg.Surface(screen.get_size(), (0,0))
        self.selection_surface = pg.Surface(screen.get_size(), (0,0))
        self.movement_surface = pg.Surface(screen.get_size(), (0,0))
        self.character_surface = pg.Surface(screen.get_size(), (0,0))
        self.ability_surface = pg.Surface(screen.get_size(), (0,0))
        self.ui_surface = pg.Surface(screen.get_size(), (0,0))

    def render(self):
        self.screen.blit(self.tile_surface, (0,0))
        self.screen.blit(self.border_surface, (0,0))
        self.screen.blit(self.selection_surface, (0,0))
        self.screen.blit(self.movement_surface, (0,0))
        self.screen.blit(self.character_surface, (0,0))
        self.screen.blit(self.ability_surface, (0,0))
        self.screen.blit(self.ui_surface, (0,0))

