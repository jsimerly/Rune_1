from typing import Callable, Dict, Type, Tuple
from in_game.map.orientations import Orientation
from dataclasses import dataclass
from in_game.entities.buildings.building_base import Building
from in_game.entities.objectives.objective_base import Objective
from in_game.map.tile import GameTile

@dataclass
class MapLoadout:
    shape: Callable
    shape_params: Dict
    orientation: Orientation
    special_tiles: dict[Type[GameTile], list[tuple[(int,int)]]]
    buildings: dict[Type[Building], list[dict]]
    objectives: dict[Type[Objective], list[dict]]
    altars: Dict
