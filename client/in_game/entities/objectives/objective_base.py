from __future__ import annotations
from typing import List, TYPE_CHECKING, Optional, Union
from in_game.ecs.components.component_base import Component
from in_game.ecs.components.sprite_component import SpriteComponent
from in_game.ecs.entity import Entity
from in_game.ecs.components.occupier_component import OccupierComponent
from in_game.ecs.components.screen_position_component import ScreenPositionComponent
from in_game.ecs.components.visual_aura import VisualAuraComponent
import pygame as pg
from in_game.map.tile import GameTile

if TYPE_CHECKING:
    ...


class Objective(Entity):
    required_components = [SpriteComponent, OccupierComponent, ScreenPositionComponent]

    def __init__(self, entity_id:str, components: List[Component] = None) -> None:
        super().__init__(entity_id, components)

class BaseRune(Objective):
    size = (60,60)
    def __init__(self, entity_id, game_tile: GameTile, image, y_offset=0, components: list[Component]=[]) -> None:
        sprite_component = SpriteComponent(image, self.size, y_offset)
        position_component = ScreenPositionComponent(game_tile.center_pixel)
        occupier_component = OccupierComponent(tiles={game_tile})

        _components = [
            sprite_component,
            occupier_component,
            position_component,
        ] + components
    
        super().__init__(entity_id, _components)

class Rune(BaseRune):
    name = 'rune'
    size = (80, 80)
    experience_radius = 3
    def __init__(self, entity_id, game_tile: GameTile) -> None:
        y_offset = int(self.size[1] * .2)
        
        visual_aura_component = VisualAuraComponent(self.experience_radius, (0,170,255), 100, .2)
        components = [visual_aura_component]

        super().__init__(
            entity_id, 
            game_tile, 
            pg.image.load('in_game/entities/objectives/images/rune.webp'),
            y_offset=y_offset,
            components=components
        )

class LargeRuneShard(BaseRune):
    name = 'large_rune_shards'
    def __init__(self, entity_id, game_tile: GameTile) -> None:
        super().__init__(entity_id, game_tile, pg.image.load('in_game/entities/objectives/images/large_runic_shards.webp'))

class SmallRuneShard(BaseRune):
    name = 'large_rune_shards'
    def __init__(self, entity_id, game_tile: GameTile) -> None:
        super().__init__(entity_id, game_tile, pg.image.load('in_game/entities/objectives/images/small_runic_shards.webp'))