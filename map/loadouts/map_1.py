
from hex import Layout, orientation_pointy, Point
from settings import SCREEN_HEIGHT, SCREEN_WIDTH
from map.tiles import *
from map.loadouts.map_layout import MapLayout

orientation=orientation_pointy
size = Point(36, 36)
origin = Point(SCREEN_WIDTH//2, SCREEN_HEIGHT//2)

layout = Layout(
    orientation=orientation,
    size=size,
    origin=origin,
)
shape=layout.hexagon
shape_params = {
    'radius' : 9,
}

special_tiles = {
    Tree: [(2,0), (1,1), (2,-1)],
    Brush: [(0,2)]
}

map_1 = MapLayout(
    layout=layout,
    shape=shape,
    shape_params=shape_params,
    special_tiles=special_tiles
)