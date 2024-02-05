
from __future__ import annotations
from typing import Tuple, Dict, TYPE_CHECKING
from in_game.ecs.ecs_manager import ECSManager
from in_game.event_bus import EventBus
from in_game.action_state import ActionStateManager
from in_game.map.tiles import Grass
from in_game.entities.ui_objects.ui_object_base import SpawningButton
from in_game.map.loadouts.map_1 import map_1
from in_game.map.map import GameMap
from in_game.client_state import InGameState
from in_game.entities.ui_objects.spawn_icon_map import spawn_icon_map

if TYPE_CHECKING:
    from entities.buildings.building_base import Building
    from entities.objectives.objective_base import Objective
    from map.loadouts.loadout_base import MapLoadout
    from map.tile import GameTile

    from event_bus import EventBus

class GameFactory:
    @staticmethod
    def create(game_data) -> InGameState:

        map_loadout = map_1 # this wil leventually come from the data
        event_bus = EventBus()
        action_state = ActionStateManager(event_bus)
        ecs_manager = ECSManager(event_bus, action_state)
        map = GameMap(map_loadout, ecs_manager, event_bus)
        ...

        def add_tile_to_ecs(entity_id, tile: GameTile):
            ecs_manager.tile_sprite_system.add_entity(tile)
            ecs_manager.border_system.add_entity(tile)
            ecs_manager.occupancy_system.add_entity(tile)
            ecs_manager.add_entity(entity_id, tile)

        ''' ----------- Creating the Game -------------- '''

        ''' Creating the Characters '''

        characters_ids = {
            'crud', 'emily', 'tim'
        }

        ''' Creating Tiles'''
        hexes = map_loadout.shape(**map_loadout.shape_params)

        for TileClass, coords in map_loadout.special_tiles.items():
            for hex in coords:
                entity_id = f'tile_{hex[0]}_{hex[1]}'
                tile = TileClass(hex[0], hex[1], map, entity_id)
                map.tiles[hex] = tile
                add_tile_to_ecs(entity_id, tile)

        for hex in hexes:
            if hex not in map.tiles:
                entity_id = f'tile_{hex[0]}_{hex[1]}'
                tile = Grass(hex[0], hex[1], map, entity_id)
                map.tiles[hex] = tile
                add_tile_to_ecs(entity_id, tile)

        ''' Creating Buildings, Objectives, and Altars'''

        for BuildingClass, data_list in map_loadout.buildings.items():
            for i, data in enumerate(data_list):
                is_team_1: bool = data['is_team_1']
                hex: tuple(int,int) = data['hex']
                team_1_id = 1
                team_2_id = 2 #these will come as params eventually
                team_id = team_1_id if is_team_1 else team_2_id
                entity_id = f'team_{team_id}_{BuildingClass.name}_{i+1}'
                if isinstance(hex, list):
                    on_tiles = [map.tiles[single_hex] for single_hex in hex]
                    
                    building = BuildingClass(entity_id, on_tiles, team_id, is_team_1, )
                    ecs_manager.building_sprite_system.add_entity(building)
                    ecs_manager.add_entity(entity_id, building)

                    for on_tile in on_tiles:
                        ecs_manager.occupancy_system.add_occupant(on_tile, building)
                else:
                    on_tile = map.tiles[hex]
                    building = BuildingClass(entity_id, on_tile, team_id, is_team_1)
                    ecs_manager.building_sprite_system.add_entity(building)
                    ecs_manager.occupancy_system.add_occupant(on_tile, building)

        for ObjectiveClass, data_list in map_loadout.objectives.items():
            for i, data in enumerate(data_list):
                hex: tuple(int, int) = data['hex']
                entity_id = f'team_{team_id}_{ObjectiveClass.name}_{i+1}'

                on_tile = map.tiles[hex]
                objective = ObjectiveClass(entity_id, on_tile)
                ecs_manager.objective_sprite_system.add_entity(objective)
                ecs_manager.add_entity(entity_id, objective)
                ecs_manager.occupancy_system.add_occupant(on_tile, objective)

        ''' Creating UI '''
        
        x_pos = 100
        y_pos = 100
        for character_id in characters_ids:
            image = spawn_icon_map[character_id]
            pos = (x_pos, y_pos)
            entity_id = f'spawn_button_{character_id}'
            spawning_button = SpawningButton(entity_id, image, pos, character_id)
            ecs_manager.ui_system.add_entity(spawning_button)
            print('yes')
            y_pos += SpawningButton.size[1] + 5


        ''' Create the InGame '''
        game_state = InGameState(event_bus, action_state, ecs_manager, map)
        return game_state

        



