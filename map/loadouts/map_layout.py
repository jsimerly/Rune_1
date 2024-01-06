from map.game_tile import GameTile
from map.tiles import *
from hex import Layout
from typing import Dict, Tuple

class MapLayout:
    def __init__(self,
        layout: Layout,
        shape,
        shape_params,
        special_tiles,
    ):
        self.layout = layout
        self.shape = shape
        self.shape_params = shape_params
        self.special_tiles = special_tiles

    #could handle random map elements
    def generate_map(self, screen, coords_on=False) -> Dict[Tuple[int, int], GameTile]:
        hexes = self.shape(**self.shape_params)

        game_map = {}
        for hex in hexes:
            game_map[(hex.q, hex.r)] = Grass(hex.q, hex.r, self.layout, screen, has_coords=coords_on)

        for tile_class, coords in self.special_tiles.items():
            for cord in coords:
                q, r = cord
                game_map[(q,r)] = tile_class(q, r, self.layout, screen, has_coords=coords_on)

        return game_map