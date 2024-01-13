from __future__ import annotations
from .abstact_component import AbstactComponent
from typing import TYPE_CHECKING, Any, List, Set, Optional, Dict
from map.game_map import GameMap  
from utils import time_it
from client.surfaces import GameSurfaces
import pygame as pg

if TYPE_CHECKING:
    from character.abs_character import AbstractCharacter
    from map.game_tile import GameTile

    
class MovementQueue:
    def __init__(self):
        self.queue: Optional[List[GameTile]] = []

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

    def remove_tile(self, tile:GameTile):
        self.queue.remove(tile)

    def remove_end_tile(self):
        self.queue.pop()
        
    def set_queue(self, tiles: List[GameTile]):
        self.queue = tiles

    def set_queue_to(self, start_tile: GameTile, end_tile: GameTile) -> bool:
        self.queue = astar(start_tile, end_tile)

    def clear(self):
        self.queue = []

class MovementComponent(AbstactComponent):
    def __init__(self, character: AbstractCharacter) -> None:
        super().__init__()
        self.character = character
        self.range = 5
        self.queue: MovementQueue = MovementQueue()

        game_surfaces = GameSurfaces()
        self.movement_surface = game_surfaces.movement_surface
        self.border_surface = game_surfaces.border_surface
        self.path_surface = pg.Surface(self.movement_surface.get_size(), pg.SRCALPHA)
        self.path_surface.set_alpha(150)

        self.line_rect = None

    ''' Movement '''
    def move(self, end_tile:GameTile) -> List[GameTile]:
        start_tile = self.character.current_tile
        self.queue.set_queue_to(start_tile, end_tile)
        self.draw_movement()
        return self.queue()
    
    def clear_move(self):
        self.queue.clear()
        self.undraw_movement()
    
    ''' Draw '''
    def draw_movement(self):
        if len(self.queue()) >= 2:
            tile_centers = []
            for tile in self.queue():
                tile_centers.append(tile.center_pixel)

            pg.draw.lines(
                self.path_surface, 
                self.character.color, 
                False, tile_centers, 3
            )
            
            self.movement_surface.blit(self.path_surface, (0,0))

    def undraw_movement(self):
        empty = pg.Color(0,0,0,0)
        clear_surface = pg.Surface(self.path_surface.get_size(), pg.SRCALPHA)
        clear_surface.set_alpha(150)
        clear_surface.fill(empty)
        clear_surface.set_alpha(None)

        self.path_surface.blit(clear_surface, (0,0))
        self.movement_surface.blit(self.path_surface, (0,0))

        # empty = pg.Color(0,0,0,0)
        # self.path_surface.fill(empty)
        # self.path_surface.set_alpha(None)
        # self.movement_surface.blit(self.path_surface, (0,0))
        # self.path_surface.set_alpha(150)

    def draw_reachable(self):
        pass

    ''' Algos '''
    def find_possible_tiles(self):
        possible = self.hex_reachable()
        return possible

    def hex_reachable(self, start_tile: GameTile) -> Set[GameTile]:
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

class Node:
    def __init__(self, parent=None, tile: GameTile=None):
        self.parent = parent
        self.tile = tile

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other: GameTile) -> bool:
        return self.tile == other.tile

@time_it
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


                



        


    
        