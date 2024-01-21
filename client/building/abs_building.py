from __future__ import annotations
from abc import ABC, abstractmethod
from components.sprite import SpriteComponent
import pygame as pg
from team.team import Team
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from map.game_tile import GameTile
    from components.map_interaction import MapInteractionComponent
    from components.spawning import SpawningComponent

class AbstractBuilding(ABC):
    def __init__(self, tile: GameTile, team_id) -> None:
        self.tile: GameTile = tile
        self.team_id = team_id
        self.map_interaction: MapInteractionComponent
        self.spawning: SpawningComponent
        self.sprite: SpriteComponent

    @property
    def team(self):
        return self._team

    @team.setter
    def team(self, value):
        self._team = value

    def set_team(self, team: Team):
        self.team = team

    def set_sprite_comp(self, image: pg.Surface):
        self.sprite = SpriteComponent(image)

    def set_tile(self, tile: GameTile):
        self.tile = tile

    def open_image(self, image_path) -> pg.image:
        return pg.image.load(image_path).convert_alpha()

    def draw(self, screen: pg.Surface):
        self.sprite.draw(screen)
