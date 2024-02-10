from __future__ import annotations
from in_game.event_bus import EventBus
from in_game.ecs.systems.system_base import System
from in_game.ecs.components.movement_component import MovementComponent
from in_game.ecs.components.resource_component import ResourceComponent
from in_game.ecs.components.occupier_component import OccupierComponent
from in_game.ecs.components.visual_edge_component import VisualHexEdgeComponent
from in_game.ecs.components.map_interaction_component import TileMapInteractionComponent
from in_game.entities.characters.character_base import Character
from in_game.map.tile import GameTile
from in_game.ecs.entity import Entity

class MovementSystem(System):
    required_components = [MovementComponent]

    def __init__(self, event_bus: EventBus) -> None:
        super().__init__(event_bus)
        self.event_bus.subscribe('character_selected', self.character_selected)
        self.event_bus.subscribe('attempt_move_to_tile', self.check_legal_move)
        self.event_bus.subscribe('attempt_drag_to_tile', self.check_legal_drag)
        self.event_bus.subscribe('spawn_to_tile', self.reset_movement_of_entity)
        self.event_bus.subscribe('idle_enter', self.clear)

        self.current_entity: Entity | None = None

    def clear(self, **kwargs):
        self.current_entity = None

    def reset_movement_of_entity(self, entity: Entity, **kwargs):
        if entity.has_component(MovementComponent):
            movement_comp: MovementComponent = entity.get_component(MovementComponent)

            len_queue = len(movement_comp.movement_queue) - 1
            if len_queue > 0:
                if entity.has_component(ResourceComponent):
                    resource_comp: ResourceComponent = entity.get_component(ResourceComponent)
                    resource_comp.amount += len_queue * movement_comp.movement_cost
            
            movement_comp.movement_queue = []

    def character_selected(self, character: Character):
        self.current_entity= character    
        possible_tiles = self.find_possible_tiles(character)

        possible_tiles = self.find_possible_tiles(self.current_entity)
        self.event_bus.publish('tile_in_movement_range', tiles=possible_tiles)
        

    def check_legal_move(self, tile: GameTile):
        if self.current_entity.has_component(ResourceComponent):
            possible_tiles = self.find_possible_tiles(self.current_entity)
            if tile in possible_tiles:
                occupier_comp: OccupierComponent = self.current_entity.get_component(OccupierComponent)
                movement_comp: MovementComponent = self.current_entity.get_component(MovementComponent)
                resource_comp: ResourceComponent = self.current_entity.get_component(ResourceComponent)

                first_tile = next(iter(occupier_comp.tiles))
                path = astar(first_tile, tile)
                movement_comp.movement_queue = path
                resource_comp.amount -= len(path)-1 * movement_comp.movement_cost

                self.event_bus.publish(
                    'entity_moved_to_tile', 
                    entity=self.current_entity,
                    from_tile = first_tile,
                    to_tile=tile 
                )

    def check_legal_drag(self, tile: GameTile) -> bool:
        if self.current_entity.has_component(ResourceComponent):
            resource_comp: ResourceComponent = self.current_entity.get_component(ResourceComponent)
            movement_comp: MovementComponent = self.current_entity.get_component(MovementComponent)
            tile_map_interaction_comp: TileMapInteractionComponent = tile.get_component(TileMapInteractionComponent)

            moves_left = resource_comp.amount // movement_comp.movement_cost
            if moves_left > 0 and tile_map_interaction_comp.is_passable: 
                if len(movement_comp.movement_queue) == 0:
                    occupier_comp: OccupierComponent = self.current_entity.get_component(OccupierComponent)
                    first_tile = next(iter(occupier_comp.tiles))
                    movement_comp.movement_queue.append(first_tile)

                if len(movement_comp.movement_queue) >= 2:
                    if tile == movement_comp.movement_queue[-2]:
                        from_tile = movement_comp.movement_queue.pop()
                        resource_comp.amount += movement_comp.movement_cost
                        self.event_bus.publish(
                            'entity_dragged_to_tile', 
                            entity=self.current_entity,
                            from_tile = from_tile,
                            to_tile = movement_comp.movement_queue[-1], 
                        )

                        possible_tiles = self.find_possible_tiles(self.current_entity)
                        self.event_bus.publish('tile_in_movement_range', tiles=possible_tiles)
                
                if len(movement_comp.movement_queue) >= 1:
                    if tile != movement_comp.movement_queue[-1] and movement_comp.movement_queue[-1] in tile.get_all_neighbors():
                        movement_comp.movement_queue.append(tile)
                        resource_comp.amount -= movement_comp.movement_cost
                        self.event_bus.publish(
                            'entity_dragged_to_tile', 
                            entity=self.current_entity,
                            from_tile = movement_comp.movement_queue[-2],
                            to_tile=tile 
                        )

                        possible_tiles = self.find_possible_tiles(self.current_entity)
                        self.event_bus.publish('tile_in_movement_range', tiles=possible_tiles)

                
    def find_possible_tiles(self, entity: Entity) -> set[GameTile]:
        occupancy_comp: OccupierComponent = entity.get_component(OccupierComponent)
        movement_comp: MovementComponent = entity.get_component(MovementComponent)
        resource_comp: ResourceComponent = entity.get_component(ResourceComponent)

        possible_tiles = set()
        for start_tile in occupancy_comp.tiles:
            max_range =  resource_comp.amount // movement_comp.movement_cost
            _possible_tiles = find_reachable_tiles(start_tile, max_range)
            possible_tiles.update(_possible_tiles)
        return possible_tiles

class Node:
    def __init__(self, parent=None, tile:GameTile=None) -> None:
        self.parent = parent
        self.tile = tile
        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other: Node) -> bool:
        return self.tile == other.tile
    
def find_reachable_tiles(start_tile: GameTile, max_range: int) -> set[GameTile]:
    ''' A DFS algo that helps us find what tile we're able to get to.'''
    max_move = max_range
    visited: set[GameTile] = set()
    visited.add(start_tile)
    fringes: list[list[GameTile]] = []
    fringes.append([start_tile])

    movement_range: dict[GameTile, int] = {start_tile: max_move}

    for k in range(1, max_move+1):
        fringes.append([])
        for tile in fringes[k-1]:
            neighbors = tile.get_all_neighbors()
            for neighbor_tile in neighbors:
                map_interaction_comp: TileMapInteractionComponent = neighbor_tile.get_component(TileMapInteractionComponent)
                #should we check this route
                if all([
                    neighbor_tile not in visited,
                    map_interaction_comp.is_passable
                ]):
                    movment_cost = 2 if map_interaction_comp.is_slowing else 1
                    remaining_moves = movement_range[tile] - movment_cost

                    if remaining_moves >= 0:
                        if map_interaction_comp.can_end_on:
                            visited.add(neighbor_tile)
                        movement_range[neighbor_tile] = remaining_moves
                        fringes[k].append(neighbor_tile)

    return visited

def astar(start_Tile: GameTile, target_tile: GameTile) -> list[GameTile] | None:
    ''' This is just used to find the quickest path to a tile, it does not handle resource costs.'''
    start_node = Node(None, start_Tile)
    end_node = Node(None, target_tile)

    open_list: list[Node] = []
    closed_list: list[Node] = []
    open_list.append(start_node)

    while len(open_list) > 0:
        current_node: Node = open_list[0]
        current_index = 0

        #decide which node to search this time based on f value
        for index, node in enumerate(open_list):
            if node.f < current_node.f:
                current_node = node
                current_index = index

        #move the current node from the open_list to the closed_list
        open_list.pop(current_index)
        closed_list.append(current_node)

        #check if we've found the node we are looking for.
        if current_node == end_node:
            path = []
            current = current_node
            while current:
                path.append(current.tile)
                current = current.parent

            return path[::-1] #reverse the order for the movement queue
        
        #find the next tile options from current node
        children: list[Node] = []
        neighors = current_node.tile.get_all_neighbors() 
        for neighbor_tile in neighors:
            map_interaction_comp: TileMapInteractionComponent = neighbor_tile.get_component(TileMapInteractionComponent)

            # skip if we can't pass through
            if not map_interaction_comp.is_passable:
                continue

            new_node = Node(parent=current_node, tile=neighbor_tile)
            children.append(new_node)

        for child in children:
            #check if we've already searched this node before (maybe should just use a set instead)
            skip_child = False
            for open_node in open_list:
                if child == open_node:
                    skip_child = True

            if skip_child:
                continue

            for closed_child in closed_list:
                if child == closed_child:
                    continue

            #handle heurstics and slowing
            g_mod = 2 if map_interaction_comp.is_slowing else 1
            child.g = current_node.g + g_mod
            child.h = distance_heuristic(child.tile, target_tile) #how far are we still fro mthe current tile
            child.f = child.g + child.h
            open_list.append(child)
    return None
        

def distance_heuristic(current_tile: GameTile, target_tile: GameTile):
    distance = current_tile.distance_to(target_tile)
    return distance

                



