from __future__ import annotations

from pygame import image as image
from building.abs_building import AbstractBuilding
from components.sprite import SpriteComponent
from components.map_interaction import MapInteractionComponent
from components.spawning_component import SpawningComponent
from typing import TYPE_CHECKING, List
import pygame as pg

from map.game_tile import GameTile

if TYPE_CHECKING:
    from team.team import Team
    from map.game_tile import GameTile

class MainBaseSprite(SpriteComponent):
    NORMAL_SIZE = (75, 75)

class MainBaseSpawning(SpawningComponent):
    def find_spawnable(self) -> List[GameTile]:
        options = []
        for q in range(-self.radius, self.radius): #we removed the +1 to make the center 3 tiles instead of 1
            r1 = max(-self.radius, -q - self.radius)
            r2 = min(self.radius, -q + self.radius)
            for r in range(r1, r2):
                tile_cords = (self.center_tile.q + q, self.center_tile.r + r)
                if tile_cords in self.center_tile.tile_map:
                    tile = self.center_tile.tile_map[tile_cords]
                    if tile.map_interaction.can_end_on:
                        options.append(tile)

        return options

class MainBase(AbstractBuilding):
    def __init__(self, tiles: List[GameTile], team_id:int) -> None:
        self.tiles: List[GameTile] = tiles
        self.team_id = team_id
        self.team: Team = None

        self.map_interaction = MapInteractionComponent(
            is_passable = False,
            can_pierce = True,
            can_end_on = False,
            blocks_vision = False,
            hides_occupants = False,
            is_slowing = False,
            walkthrough_effects = None,
        )

        image = self.open_image('building/main_base/gui/main_base.webp')
        self.sprite: SpriteComponent = MainBaseSprite(image)
        x, y = 0, 0
        for tile in self.tiles:
            x += tile.center_pixel[0]
            y += tile.center_pixel[1]
        x = x//3 
        y = y//3 - 15
        self.sprite.move_to_pixel((x,y))
        self.spawning = MainBaseSpawning(radius=4, center_tile=tiles[0])

    def set_team(self, team:Team):
        self.team = team