from .loadouts.loadout_base import MapLoadout
from .tiles import *
from typing import Tuple, Dict
from .tile import GameTile
from in_game.ecs.components.occupancy_component import OccupancyComponent
from in_game.ecs.components.occupier_component import OccupierComponent

class TileFactory:
    @staticmethod
    def create_map(map, map_loadout: MapLoadout) -> Dict[Tuple[int,int],GameTile]:

        hexes = map_loadout.shape(**map_loadout.shape_params)
        tiles: Dict[Tuple[int,int], GameTile] = {}
        for hex in hexes:
            tiles[hex] = Grass(hex[0], hex[1], map)

        for TileClass, coords in map_loadout.special_tiles.items():
            for hex in coords:
                tiles[hex] = TileClass(hex[0], hex[1], map)

        for BuildingClass, coords in map_loadout.buildings.items():
            for hex in coords:
                tiles[hex].get_component()

        return tiles


