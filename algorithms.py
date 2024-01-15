from __future__ import annotations
from typing import TYPE_CHECKING, Set, List, Dict, Optional

if TYPE_CHECKING:
    from map.game_tile import GameTile


def hex_reachable(start_tile: GameTile, max_range:int) -> Set[GameTile]:
    max_move = max_range

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
                    neighbor_tile.map_interaction.is_passable,
                ]):
                    remaining_move = movement_range[tile] - neighbor_tile.map_interaction.movement_cost
                    if remaining_move >= 0:
                        if neighbor_tile.map_interaction.can_end_on:
                            visited.add(neighbor_tile)
                        movement_range[neighbor_tile] = remaining_move
                        fringes[k].append(neighbor_tile)
    return visited


class Node:
    def __init__(self, parent=None, tile: GameTile=None):
        self.parent = parent
        self.tile = tile

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other: GameTile) -> bool:
        return self.tile == other.tile


def astar(start_tile: GameTile, target_tile: GameTile) -> Optional[List[GameTile]]:
    start_node = Node(None, start_tile)
    start_node.g, start_node.h, start_node.f = 0, 0, 0
    end_node = Node(None, target_tile)
    end_node.g, end_node.h, end_node.f = 0, 0 ,0

    open_list: List[Node] = []
    closed_list: List[Node] = []

    open_list.append(start_node)

    hold = 0
    while len(open_list) > 0:
        hold+=1
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
            skip_child = False # used to handle if we need to append or not
            for open_node in open_list:
                if child == open_node:
                    skip_child = True
                    break

            if skip_child:
                continue

            for closed_child in closed_list:
                if child == closed_child:
                    continue
            
            #to handle is_slowing we'll add 2 instead of 1
            g_mod = current_node.tile.map_interaction.movement_cost
            child.g = current_node.g + g_mod
            child.h = distance_heuristic(child.tile, target_tile)

            child.f = child.g + child.h
            open_list.append(child)

    return []

def distance_heuristic(current_tile: GameTile, target_tile: GameTile):
    distance = current_tile.distance_to(target_tile)
    return distance

        