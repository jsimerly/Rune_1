from __future__ import annotations
from abc import ABC, abstractmethod
from components.sprite import SpriteComponent
import pygame as pg
from team.team import Team
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from map.game_tile import GameTile
    from components.map_interaction import MapInteractionComponent

class AbstractBuilding(ABC):
    def __init__(self) -> None:
        self.tile = None
        self.map_interaction: MapInteractionComponent

    @property
    def team(self):
        return self._team

    @team.setter
    def team(self, value):
        self._team = value

    @property
    def is_passable(self):
        return self._is_passable

    @is_passable.setter
    def is_passable(self, value):
        self._is_passable = value

    @property
    def can_pierce(self):
        return self._can_pierce

    @can_pierce.setter
    def can_pierce(self, value):
        self._can_pierce = value

    @property
    def can_end_on(self):
        return self._can_end_on

    @can_end_on.setter
    def can_end_on(self, value):
        self._can_end_on = value

    @property
    def blocks_vision(self):
        return self._blocks_vision

    @blocks_vision.setter
    def blocks_vision(self, value):
        self._blocks_vision = value

    @property
    def hides_occupants(self):
        return self._hides_occupants

    @hides_occupants.setter
    def hides_occupants(self, value):
        self._hides_occupants = value

    @property
    def is_slowing(self):
        return self._is_slowing

    @is_slowing.setter
    def is_slowing(self, value):
        self._is_slowing = value

    @property
    def walkthrough_effects(self):
        return self._walkthrough_effects

    @walkthrough_effects.setter
    def walkthrough_effects(self, value):
        self._walkthrough_effects = value


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
