from __future__ import annotations
from typing import List, TYPE_CHECKING, Optional, Union
from in_game.ecs.components.component_base import Component
from in_game.ecs.components.sprite_component import SpriteComponent
from in_game.ecs.entity import Entity
from in_game.ecs.components.occupier_component import OccupierComponent
from in_game.ecs.components.screen_position_component import ScreenPositionComponent
import pygame as pg
from in_game.map.tile import GameTile

if TYPE_CHECKING:
    ...


class Objective(Entity):
    required_components = [SpriteComponent, OccupierComponent, ScreenPositionComponent]

    def __init__(self, components: List[Component] = None) -> None:
        super().__init__(components)

class BaseRune(Objective):
    size = (60,60)
    def __init__(self, game_tile: GameTile, image) -> None:
        sprite_component = SpriteComponent(image, self.size)
        position_component = ScreenPositionComponent(game_tile.center_pixel, self.size)
        occupier_component = OccupierComponent(tiles={game_tile})

        components = [
            sprite_component,
            occupier_component,
            position_component,
        ]
        super().__init__(components)

class Rune(BaseRune):
    size = (80, 80)
    def __init__(self, game_tile: GameTile) -> None:
        super().__init__(game_tile, pg.image.load('in_game/entities/objectives/images/rune.webp'))

class LargeRuneShard(BaseRune):
    def __init__(self, game_tile: GameTile) -> None:
        super().__init__(game_tile, pg.image.load('in_game/entities/objectives/images/large_runic_shards.webp'))

class SmallRuneShard(BaseRune):
    def __init__(self, game_tile: GameTile) -> None:
        super().__init__(game_tile, pg.image.load('in_game/entities/objectives/images/small_runic_shards.webp'))