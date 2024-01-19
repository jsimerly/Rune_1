from __future__ import annotations
from typing import TYPE_CHECKING, List, Set

if TYPE_CHECKING:
    from character.abs_character import AbstractCharacter
    from building.abs_building import AbstractBuilding
    from map.game_tile import GameTile

class Team:
    def __init__(self, team_id:int) -> None:
        self.team_id = team_id
        self.characters: List[AbstractCharacter] = []
        self.buildings: List[AbstractBuilding] = []

    def add_character(self, character: AbstractCharacter):
        self.characters.append(character)

    def add_building(self, building: AbstractBuilding):
        self.buildings.append(building)

    def remove_building(self, building: AbstractBuilding):
        self.buildings.remove(building)

    def get_spawnable_tiles(self):
        spawnable_tiles: Set[GameTile] = set()
        for character in self.characters:
            if hasattr(character, 'spawning'):
                character.spawning.find_spawnable()

        for building in self.buildings:
            options = building.spawning.find_spawnable()
            spawnable_tiles.update(options)

        return spawnable_tiles
    


