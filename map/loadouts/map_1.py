
from hex import Layout, orientation_pointy, Point
from settings import SCREEN_HEIGHT, SCREEN_WIDTH
from map.tiles import *
from building.pylon.pylon import Pylon
from building.main_base.main_base import MainBase
from map.loadouts.map_layout import MapLayout
from objective.runes.rune.rune import Rune

orientation=orientation_pointy
size = Point(36, 36)
origin = Point(1000, SCREEN_HEIGHT//2)

layout = Layout(
    orientation=orientation,
    size=size,
    origin=origin,
)
shape=layout.hexagon
shape_params = {
    'radius' : 8,
}

special_tiles = {
    Tree: [(2,0), (1,1), (2,-1)],
    # Brush: [(0,2)],
    RoughTerrian: [(0,2)],
}

team_1_buildings = {
    Pylon: [(-5,4), (1,4)]
}
team_1_main_base = [(-3,6), (-4, 7), (-3,7)]

team_2_buildings = {
    Pylon: [(0,4)]
}

team_2_main_base = [(2,-5), (2,-6), (3,-6)]

image_path = 'objective/runes/rune/gui/rune_std.webp'
objectives = [
    {
        'class': Rune,
        'tile': (-3,0),
        'radius': 3,
        'power': 334,
        'image_path': image_path,
    }
]


map_1 = MapLayout(
    layout=layout,
    shape=shape,
    shape_params=shape_params,
    special_tiles=special_tiles,
    team_1_buildings=team_1_buildings,
    team_1_main_base=team_1_main_base,
    team_2_buildings=team_2_buildings,
    team_2_main_base=team_2_main_base,
    objectives=objectives
)