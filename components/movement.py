from __future__ import annotations
from .abstact_component import AbstactComponent
from typing import TYPE_CHECKING, List, Set, Optional, Dict
from map.game_map import GameMap  
if TYPE_CHECKING:
    from character.abs_character import AbstractCharacter
    from map.game_tile import GameTile


class Node():
    def __init__(self, parent=None, tile: GameTile=None):
        self.parent = parent
        self.tile = tile

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other: GameTile) -> bool:
        return self.tile == other.tile

class MovementComponent(AbstactComponent):
    def __init__(self, character: AbstractCharacter, game_map: GameMap) -> None:
        super().__init__()
        self.character = character
        self.game_map = game_map
        self.range = 5
        self.queued_movement: List[GameTile] = []

    def move_character_to(self, tile: GameTile):
        travel_path = self.astar(tile)
        self.queued_movement = travel_path
        self.draw_queued_movement()


    def draw_queued_movement(self):
        self.game_map.draw_movement_path(self.queued_movement)


    def find_possible_tiles(self):
        possible = self.hex_reachable()
        return possible
    
    #needs updated to handle rough terrain
    def hex_reachable(self) -> Set[GameTile]:
        start_tile = self.character.current_tile
        max_move = self.range

        visited: Set[GameTile] = set()
        visited.add(start_tile)
        fringes: List[List[GameTile]] = []
        fringes.append([start_tile])

        movement_range: Dict[GameTile, int] = {start_tile: max_move}

        for k in range(1, max_move+1):
            fringes.append([])
            for tile in fringes[k-1]:
                neighbors = tile.get_all_neighbor_tiles()
                for neighbor_tile in neighbors:
                    if all([
                        neighbor_tile not in visited,
                        tile.map_interaction.is_passable
                    ]):
                        remaining_move = movement_range[tile] - neighbor_tile.map_interaction.movement_cost
                        if remaining_move >= 0:
                            if neighbor_tile.map_interaction.can_end_on:
                                visited.add(neighbor_tile)
                                movement_range[neighbor_tile] = remaining_move
                            fringes[k].append(neighbor_tile)

        return visited

    def astar(self, target_tile: GameTile) -> Optional[List[GameTile]]:
        start_node = Node(None, self.character.current_tile)
        start_node.g, start_node.h, start_node.f = 0, 0, 0
        end_node = Node(None, target_tile)
        end_node.g, end_node.h, end_node.f = 0, 0 ,0

        open_list: List[Node] = []
        closed_list: List[Node] = []

        open_list.append(start_node)

        while len(open_list) > 0:
            current_node: Node = open_list[0]
            current_index = 0

            for index, node in enumerate(open_list):
                if node.f < current_node.f:
                    current_node = node
                    current_index = index

            open_list.pop(current_index)
            closed_list.append(current_node)

            if current_node == end_node:
                path = []
                current = current_node
                while current:
                    path.append(current.tile)
                    current = current.parent
                return path[::-1] # reversing the list so we have start values in front
            
            children: List[Node] = []
            neighbors = current_node.tile.get_all_neighbor_tiles()
            for neighbor_tile in neighbors:
                #skip this tile if we can't pass through it.
                if not neighbor_tile.map_interaction.is_passable:
                    continue

                #create new node
                new_node = Node(parent=current_node, tile=neighbor_tile) 
                children.append(new_node)


            for child in children:
                for closed_child in closed_list:
                    if child == closed_child:
                        continue
                
                #to handle is_slowing we'll add 2 instead of 1
                g_mod = current_node.tile.map_interaction.movement_cost
                child.g = current_node.g + g_mod
                child.h = self.manhattan_heuristic(child.tile, target_tile)
                child.f = child.g + child.h

                for open_node in open_list:
                    if child == open_node and child.g > open_node.g:
                        continue

                open_list.append(child)

        return None

    def manhattan_heuristic(self, start_tile: GameTile, end_tile: GameTile):
        dq = end_tile.q - start_tile.q
        dr = end_tile.r - start_tile.r

        return abs(dq + dr)
                




                



        


    
        