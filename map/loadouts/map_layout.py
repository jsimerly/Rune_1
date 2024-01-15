
from map.tiles import *
from hex import Layout
from typing import Dict, Tuple, List, TYPE_CHECKING
from building.main_base.main_base import MainBase

if TYPE_CHECKING:
    from building.abs_building import AbstractBuilding
    from map.game_tile import GameTile
    from team.team import Team
class MapLayout:
    def __init__(self,
        layout: Layout,
        shape,
        shape_params,
        special_tiles,
        team_1_buildings,
        team_1_main_base,
        team_2_buildings,
        team_2_main_base,
    ):
        self.layout = layout
        self.shape = shape
        self.shape_params = shape_params
        self.special_tiles: Dict[GameTile, Tuple[int,int]] = special_tiles
        self.team_1_buildings: Dict[AbstractBuilding, Tuple[int,int]] = team_1_buildings
        self.team_1_main_base: MainBase = team_1_main_base
        self.team_2_buildings: Dict[AbstractBuilding, Tuple[int,int]] = team_2_buildings
        self.team_2_main_base: MainBase = team_2_main_base
        
    #could handle random map elements
    def generate_map(self) -> Dict[Tuple[int, int], GameTile]:
        hexes = self.shape(**self.shape_params)

        game_map: Dict[Tuple[int,int], GameTile] = {}
        for hex in hexes:
            game_map[(hex.q, hex.r)] = Grass(hex.q, hex.r, self.layout)

        for tile_class, coords in self.special_tiles.items():
            for cord in coords:
                q, r = cord
                game_map[(q,r)] = tile_class(q, r, self.layout)

        for building_class, coords in self.team_1_buildings.items():
            for cord in coords:
                tile = game_map[cord]
                building = building_class(tile, team_id=1)
                tile.add_building(building)

        base_tiles_t1: List[GameTile] = []
        for cord in self.team_1_main_base:
            tile = game_map[cord]
            base_tiles_t1.append(tile)
        main_base_t1 = MainBase(tiles=base_tiles_t1, team_id=1)

        for tile in base_tiles_t1:
            tile.add_building(main_base_t1)

        base_tiles_t2: List[GameTile] = []
        for cord in self.team_2_main_base:
            tile = game_map[cord]
            base_tiles_t2.append(tile)
        main_base_t2 = MainBase(tiles=base_tiles_t2, team_id=2) 
        for tile in base_tiles_t2:
            tile.add_building(main_base_t2)


        return game_map