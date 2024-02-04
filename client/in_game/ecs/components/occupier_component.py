from __future__ import annotations
from in_game.ecs.components.component_base import Component
from typing import Tuple, List, TYPE_CHECKING
from dataclasses import dataclass

if TYPE_CHECKING:
    from ecs.entity import Entity
    from map.tile import GameTile

@dataclass
class OccupierComponent(Component):
    tiles: List[Entity] | None
