from typing import Callable, Dict
from in_game.map.orientations import Orientation
from dataclasses import dataclass

@dataclass
class MapLoadout:
    shape: Callable
    shape_params: Dict
    orientation: Orientation
    special_tiles: Dict
    buildings: Dict
    objectives: Dict
    altars: Dict
