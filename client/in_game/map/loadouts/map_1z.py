
from hex import Layout, orientation_pointy, Point
from settings import SCREEN_HEIGHT, SCREEN_WIDTH
from in_game.map.tiles import *
from building.pylon.pylon import Pylon
from building.main_base.main_base import MainBase
from in_game.map.loadouts.map_layout import MapLayout
from objective.runes.rune.rune import Rune
from objective.runes.shards.shards import RuneShards

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
    Tree: [
        (1, -1), (1, 0), (0, 1), (2,-1), (1,1), (-1,2), (1, -2), # Median
        (1,3), (1,4), (3,3), (5,-4), (4,-3), (6,-3), # center camp
        (5,-1), (5,0), (4,1), #right camp
        (1,6), (0,7), (-1, 7), (7,-6), (7,-7), (6,-7), #right corner
        (-2,4), (2,-4) # lone tree
    ],
    Brush: [
        (6,1), (7,-1), (7,0), 
        (5,2), (4,3), (3,4),(2,4), (2,5), 
        (7, -2), (7,-3), (7,-4), (7,-5), (6,-4)
    ],
    RoughTerrian: [],
}

team_1_buildings = {
    Pylon: [(-5,4), (-2,6)]
}
team_1_main_base = [(-5,6), (-6, 7), (-5,7)]

team_2_buildings = {
    Pylon: [(0,4)]
}

team_2_main_base = [(0,-7), (-1,-6), (0,-6)]

rune_image_path = 'objective/runes/rune/gui/rune_std.webp'
lg_shard_path = 'objective/runes/shards/gui/large_crystals.webp'
sm_shard_path = 'objective/runes/shards/gui/small_crystals.webp'
objectives = [
    {
        'class': Rune,
        'tile': (-3,0),
        'radius': 3,
        'power': 334,
        'image_path': rune_image_path,
    },
    {
        'class': RuneShards, 'tile': (0, 2),
        'respawn_rate' : 2,'power': 250,
        'image_path': sm_shard_path,
    },
    {
        'class': RuneShards, 'tile': (2, -2),
        'respawn_rate' : 2, 'power': 250,
        'image_path': sm_shard_path,
    },
    {
        'class': RuneShards, 'tile': (2, 3),
        'respawn_rate' : 2, 'power': 250,
        'image_path': sm_shard_path,
    },
    {
        'class': RuneShards, 'tile': (5, -3),
        'respawn_rate' : 2, 'power': 250,
        'image_path': sm_shard_path,
    },
    {
        'class': RuneShards, 'tile': (6, 0),
        'respawn_rate' : 4, 'power': 500,
        'image_path': lg_shard_path,
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