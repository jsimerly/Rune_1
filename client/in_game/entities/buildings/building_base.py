from __future__ import annotations
from typing import List, TYPE_CHECKING, Optional, Union

from in_game.ecs.components.sprite_component import SpriteComponent
from in_game.ecs.entity import Entity
from in_game.ecs.components.occupier_component import OccupierComponent
from in_game.ecs.components.screen_position_component import ScreenPositionComponent
from in_game.ecs.components.team_component import TeamComponent
from in_game.ecs.components.spawner_component import SpawnerComponent
from in_game.ecs.components.vision_component import VisionComponent
import pygame as pg
from in_game.map.tile import GameTile

if TYPE_CHECKING:
    from in_game.ecs.components.component_base import Component


class Building(Entity):
    required_components = [SpriteComponent, OccupierComponent, ScreenPositionComponent]

    def __init__(self, entity_id: str, components: List[Component] = None) -> None:
        super().__init__(entity_id, components)

    def get_center_between_tiles(self, tiles: list[GameTile]) -> tuple(int, int):
        x, y = 0, 0
        for tile in tiles:
            x += tile.center_pixel[0]
            y += tile.center_pixel[1]

        x = x//len(tiles)
        y = y//len(tiles)
        return (x,y)

class Teleporter(Building):
    size = (80, 80)
    name = 'teleporter'
    team_1_image = pg.image.load('in_game/entities/buildings/images/teleporter_1.webp')
    team_2_image = pg.image.load('in_game/entities/buildings/images/teleporter_2.webp')

    def __init__(self, 
        entity_id: str,
        game_tile: None | GameTile | set[GameTile],
        team_id : str,
        is_team_1: bool,
    ) -> None:
        if isinstance(game_tile, GameTile):
            occupier_component = OccupierComponent(tiles={game_tile})
            center_pos = game_tile.center_pixel

        if isinstance(game_tile, list):
            tiles_set = set(game_tile)
            occupier_component = OccupierComponent(tiles=tiles_set)
            center_pos = self.get_center_between_tiles(game_tile)

        if is_team_1:
            image = self.team_1_image
        else:
            image=self.team_2_image

        y_offset = int(self.size[1] * .2)
        sprite_component = SpriteComponent(image, self.size, y_offset)
        position_component = ScreenPositionComponent(center_pos)
        team_component = TeamComponent(team_id, is_team_1)
        spawner_component = SpawnerComponent(radius=3)
        vision_component = VisionComponent(vision_radius=4)

        components = [
            sprite_component, 
            occupier_component, 
            position_component, 
            team_component,
            spawner_component,
            vision_component,
        ]
        super().__init__(entity_id, components)

class Mainbase(Building):
    size = (140, 140)
    name = 'main_base'
    team_1_image = pg.image.load('in_game/entities/buildings/images/base_1.webp')
    team_2_image = pg.image.load('in_game/entities/buildings/images/base_2.webp')
    def __init__(self, entity_id:str, game_tile: None | GameTile | set[GameTile], team_id:str, is_team_1: bool):
        if isinstance(game_tile, GameTile):
            occupier_component = OccupierComponent(set(game_tile))
            center_pos = game_tile.center_pixel

        if isinstance(game_tile, list):
            tiles_set = set(game_tile)
            occupier_component = OccupierComponent(tiles=tiles_set)
            center_pos = self.get_center_between_tiles(game_tile)

        if is_team_1:
            image = self.team_1_image
        else:
            image=self.team_2_image

        y_offset = int(self.size[1] * .1)
        sprite_component = SpriteComponent(image, self.size, y_offset)
        position_component = ScreenPositionComponent(center_pos)
        team_component = TeamComponent(team_id, is_team_1)
        spawner_component = SpawnerComponent(radius=3)
        vision_component = VisionComponent(vision_radius=4)

        components = [
            sprite_component, 
            occupier_component, 
            position_component, 
            team_component,
            spawner_component,
            vision_component
        ]
        super().__init__(entity_id, components)