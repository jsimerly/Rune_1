from typing import List, TYPE_CHECKING, Optional, Union
from client.in_game.ecs.components.component_base import Component
from ecs.components.sprite_component import SpriteComponent
from ecs.entity import Entity
from ecs.components.occupier_component import OccupierComponent

if TYPE_CHECKING:
    from map.tile import GameTile


class Building(Entity):
    required_components = [SpriteComponent]

    def __init__(self, components: List[Component] = None) -> None:
        super().__init__(components)

class Teleporter(Building):
    def __init__(self, game_tile: None | GameTile | List[GameTile]) -> None:
        sprite_component = SpriteComponent('ecs/entities/buildings/images/teleporter.webp')
        if isinstance(game_tile, GameTile):
            occupier_component = OccupierComponent([game_tile])
        if isinstance(game_tile, list):
            occupier_component = OccupierComponent(game_tile)

        components = [sprite_component, occupier_component]
        super().__init__(components)

class Mainbase(Building):
    def __init__(self, game_tile: None | GameTile | List[GameTile]) -> None:
        sprite_component = SpriteComponent('ecs/entities/buildings/images/teleporter.webp')
        if isinstance(game_tile, GameTile):
            occupier_component = OccupierComponent([game_tile])
        if isinstance(game_tile, list):
            occupier_component = OccupierComponent(game_tile)

        components = [sprite_component, occupier_component]
        super().__init__(components)