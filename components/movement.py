from __future__ import annotations
from .abstact_component import AbstactComponent
from typing import TYPE_CHECKING, Any, List, Set, Optional, Dict, Tuple
from utils import time_it
from client.surfaces import GameSurfaces
import pygame as pg

if TYPE_CHECKING:
    from character.abs_character import AbstractCharacter
    from map.game_tile import GameTile

    
class MovementQueue:
    def __init__(self, color: Tuple[int,int,int]):
        self.queue: Optional[List[GameTile]] = []
        self.pixels: List[Tuple[int,int]] = []
        self.game_surfaces = GameSurfaces()
        self.color = color + (150,)

    def __call__(self) -> Optional[List[GameTile]]:
        return self.queue

    @property
    def is_empty(self) -> bool:
        return len(self.queue) == 0

    @property
    def start_tile(self) -> GameTile:
        if not self.is_empty:
            return self.queue[0]
        
    @property
    def end_tile(self) -> GameTile:
        if not self.is_empty:
            return self.queue[-1]
        
    def add_tile(self, tile:GameTile):
        self.queue.append(tile)
        self.handle_update()

    def remove_tile(self, tile:GameTile):
        self.queue.remove(tile)
        self.handle_update()

    def remove_end_tile(self):
        self.queue.pop()
        self.handle_update()
        
    def set_queue(self, tiles: List[GameTile]):
        self.queue = tiles
        self.handle_update()

    def set_queue_to(self, start_tile: GameTile, end_tile: GameTile) -> bool:
        self.queue = astar(start_tile, end_tile)
        self.handle_update()

    def clear(self):
        self.queue = []
        self.handle_update()


    ''' Draw '''
    def draw(self, screen: pg.Surface):
        if len(self.pixels) >= 2:
            trans_surface = pg.Surface(screen.get_size(), pg.SRCALPHA)
            pg.draw.lines(trans_surface, self.color, False, self.pixels, 5)
            screen.blit(trans_surface, (0, 0))

    def handle_update(self):
        if len(self.queue) >= 2:
            self.pixels = [tile.center_pixel for tile in self.queue]
            self.game_surfaces.add_to_layer(self.game_surfaces.movement, self)
        else:
            self.game_surfaces.remove_from_layer(self.game_surfaces.movement, self)


class MovementComponent(AbstactComponent):
    def __init__(self, character: AbstractCharacter) -> None:
        super().__init__()
        self.character = character
        self.range = 5
        self.queue: MovementQueue = MovementQueue(character.color)

    ''' Movement '''
    def move(self, start_tile: GameTile, end_tile:GameTile) -> List[GameTile]:
        self.queue.set_queue_to(start_tile, end_tile)
        return self.queue()
    
    def drag_move_new_tile(self, tile:GameTile):
        if len(self.queue()) >= 2:
            if tile == self.queue()[-2]:
                self.queue.remove_end_tile()

        if tile != self.queue.end_tile:
            self.queue.add_tile(tile)
    
    def clear_move(self) -> Tuple[GameTile, GameTile]:
        start_tile = self.queue.start_tile
        end_tile = self.queue.end_tile
        self.queue.clear()    
        return start_tile, end_tile

    def find_possible_tiles(self, from_tile: GameTile) -> List[GameTile]:
        possible = hex_reachable(from_tile, self.range)
        return possible

''' Algos '''


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
                    tile.map_interaction.is_passable
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

# @time_it
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


                



        


    
        