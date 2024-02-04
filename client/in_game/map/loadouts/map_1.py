from in_game.map.orientations import orientation_pointy
from in_game.map.loadouts.map_shapes import hexagon
from .loadout_base import MapLoadout
from in_game.map.tiles import *

map_1 = MapLoadout(
    shape=hexagon,
    shape_params={
    'radius' : 8
    },
    orientation=orientation_pointy,
    special_tiles={
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
    },
    buildings={},
    objectives={},
    altars={}
)