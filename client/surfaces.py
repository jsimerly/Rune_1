from .singleton import Singleton
import pygame as pg

class GameSurfaces(metaclass=Singleton):
    def __init__(self, screen: pg.Surface) -> None:
        self.screen = screen
        self.tile_surface = pg.Surface(screen.get_size(), pg.SRCALPHA)
        self.border_surface = pg.Surface(screen.get_size(), pg.SRCALPHA)
        self.selection_surface = pg.Surface(screen.get_size(), pg.SRCALPHA)
        self.movement_surface = pg.Surface(screen.get_size(), pg.SRCALPHA)
        self.character_surface = pg.Surface(screen.get_size(), pg.SRCALPHA)
        self.ability_surface = pg.Surface(screen.get_size(), pg.SRCALPHA)
        self.ui_surface = pg.Surface(screen.get_size(), pg.SRCALPHA)

    def render(self):
        self.screen.blit(self.tile_surface, (0,0))
        self.screen.blit(self.border_surface, (0,0))
        self.screen.blit(self.selection_surface, (0,0))
        self.screen.blit(self.movement_surface, (0,0))
        self.screen.blit(self.character_surface, (0,0))
        self.screen.blit(self.ability_surface, (0,0))
        self.screen.blit(self.ui_surface, (0,0))
    

