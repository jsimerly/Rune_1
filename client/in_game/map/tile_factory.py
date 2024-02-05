from __future__ import annotations
from .loadouts.loadout_base import MapLoadout
from .tiles import *
from typing import Tuple, Dict, TYPE_CHECKING
from .tile import GameTile

if TYPE_CHECKING:
    from ecs.ecs_manager import ECSManager
    from entities.buildings.building_base import Building
    from entities.objectives.objective_base import Objective

class TileFactory:
    @staticmethod
    def create_map(map, map_loadout: MapLoadout, ecs_manager: ECSManager) -> Dict[Tuple[int,int],GameTile]:
        def add_tile_to_ecs(tile: GameTile):
            ecs_manager.tile_sprite_system.add_entity(tile)
            ecs_manager.border_system.add_entity(tile)
            ecs_manager.occupancy_system.add_entity(tile)

        hexes = map_loadout.shape(**map_loadout.shape_params)
        tiles: Dict[Tuple[int,int], GameTile] = {}

        for TileClass, coords in map_loadout.special_tiles.items():
            for hex in coords:
                entity_id = f'tile_{hex[0]}_{hex[1]}'
                tile = TileClass(hex[0], hex[1], map, entity_id)
                tiles[hex] = tile

                add_tile_to_ecs(tile)
                ecs_manager.add_entity(entity_id, tile)

        for hex in hexes:
            if hex not in tiles:
                entity_id = f'tile_{hex[0]}_{hex[1]}'
                tile = Grass(hex[0], hex[1], map, entity_id)
                tiles[hex] = tile
                add_tile_to_ecs(tile)
                ecs_manager.add_entity(entity_id, tile)

        for BuildingClass, data_list in map_loadout.buildings.items():
            for i, data in enumerate(data_list):
                is_team_1: bool = data['is_team_1']
                hex: tuple(int,int) = data['hex']
                team_1_id = 1
                team_2_id = 2 #these will come as params eventually
                team_id = team_1_id if is_team_1 else team_2_id
                entity_id = f'team_{team_id}_{BuildingClass.name}_{i+1}'
                if isinstance(hex, list):
                    on_tiles = [tiles[single_hex] for single_hex in hex]
                    
                    building = BuildingClass(entity_id, on_tiles, team_id, is_team_1, )
                    ecs_manager.building_sprite_system.add_entity(building)
                    ecs_manager.add_entity(entity_id, building)

                    for on_tile in on_tiles:
                        ecs_manager.occupancy_system.add_occupant(on_tile, building)
                else:
                    on_tile = tiles[hex]
                    building = BuildingClass(entity_id, on_tile, team_id, is_team_1)
                    ecs_manager.building_sprite_system.add_entity(building)
                    ecs_manager.occupancy_system.add_occupant(on_tile, building)

        for ObjectiveClass, data_list in map_loadout.objectives.items():
            for i, data in enumerate(data_list):
                hex: tuple(int, int) = data['hex']
                entity_id = f'team_{team_id}_{ObjectiveClass.name}_{i+1}'

                on_tile = tiles[hex]
                objective = ObjectiveClass(entity_id, on_tile)
                ecs_manager.objective_sprite_system.add_entity(objective)
                ecs_manager.add_entity(entity_id, objective)
                ecs_manager.occupancy_system.add_occupant(on_tile, objective)
                  
        return tiles
    



