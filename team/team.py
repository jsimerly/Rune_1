from __future__ import annotations
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from character.abs_character import AbstractCharacter
    from building.abs_building import AbstractBuilding

class Team:
    def __init__(self) -> None:
        self.characters: List[AbstractCharacter]
        self.buildings: List[AbstractBuilding]

    def add_character(self, character: AbstractCharacter):
        self.characters.append(character)

    def add_building(self, building: AbstractBuilding):
        self.buildings.append(building)

    def remove_building(self, building: AbstractBuilding):
        self.buildings.remove(building)



