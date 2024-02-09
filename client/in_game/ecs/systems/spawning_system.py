from __future__ import annotations
from in_game.event_bus import EventBus
from in_game.ecs.systems.system_base import System
from in_game.ecs.components.spawner_component import SpawnerComponent
from in_game.ecs.components.occupier_component import OccupierComponent
from in_game.ecs.components.occupancy_component import OccupancyComponent
from in_game.ecs.components.team_component import TeamComponent
from in_game.ecs.entity import Entity
from typing import TYPE_CHECKING
from in_game.map.tile import GameTile
from in_game.ecs.components.visual_edge_component import VisualHexEdgeComponent
from in_game.ecs.components.map_interaction_component import TileMapInteractionComponent

class SpawningSystem(System):
    required_components = [OccupierComponent, SpawnerComponent]
    spawning_color = (220, 220, 255)
    spawning_thickness = 3

    def __init__(self, event_bus: EventBus) -> None:
        super().__init__(event_bus)
        self.event_bus.subscribe('spawn_button_clicked', self.handle_spawn_button_clicked)
        self.event_bus.subscribe('enter_idle', self.enter_idle)
        self.event_bus.subscribe('attempt_spawn_to_tile', self.check_for_legal_spawn)
        self.spawning_entity = None

    def enter_idle(self, _):
        self.spawning_entity = None

    def handle_spawn_button_clicked(self, entity: Entity):
        reachable_tiles = self.find_reachable_tiles(entity)

        for tile in reachable_tiles:
            edge_component: VisualHexEdgeComponent = tile.get_component(VisualHexEdgeComponent)

            edge_component.color = self.spawning_color
            edge_component.thickness = self.spawning_thickness
            edge_component.transparent = True

        self.event_bus.publish('spawning_started')
        self.spawning_entity = entity

    def find_reachable_tiles(self, spawning_entity: Entity):
        reachable_tiles: set[GameTile] = set()
        for entity in self.entities:
            if entity.has_component(TeamComponent) and spawning_entity.has_component(TeamComponent):
                spawner_team: TeamComponent = entity.get_component(TeamComponent)
                spawning_team: TeamComponent = spawning_entity.get_component(TeamComponent)

            if spawner_team.team_id != spawning_team.team_id:
                continue
            
            spawn_component: SpawnerComponent = entity.get_component(SpawnerComponent)
            occupier_component: OccupierComponent = entity.get_component(OccupierComponent)

            spawning_radius = spawn_component.radius
            tiles = occupier_component.tiles

            for tile in tiles:
                reachable = self.in_radius_end_on(tile, spawning_radius)
                reachable_tiles.update(reachable)

        return reachable_tiles
    
    def in_radius_end_on(self, center_tile: GameTile, radius:int) -> list[GameTile]:
        options = []
        for q in range(-radius, radius + 1):
            r1 = max(-radius, -q - radius)
            r2 = min(radius, -q + radius) + 1
            for r in range(r1, r2):
                tile_cords = (center_tile.q + q, center_tile.r + r)
                if tile_cords in center_tile.map.tiles:
                    tile = center_tile.map.tiles[tile_cords]
                    tile_map_inter_comp: TileMapInteractionComponent = tile.get_component(TileMapInteractionComponent)
                    if tile_map_inter_comp.can_end_on:
                        options.append(tile)

        return options

    def check_for_legal_spawn(self, tile: GameTile):    
        if tile in self.find_reachable_tiles(self.spawning_entity):
            self.event_bus.publish('spawn_to_tile', tile=tile, entity=self.spawning_entity)
        else:
            print('You cannot spawn there.')
        

        
        


    

    