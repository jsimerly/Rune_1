from __future__ import annotations
from typing import TYPE_CHECKING, List, Set, Dict
from character.abs_character import AbstractCharacter
from game.phases.spawn_handler import SpawnHandler

class Team:
    def __init__(self, team_id):
        self.team_id = team_id
        self.color: (int, int, int) = (0,0,0)

        self.characters: Set[AbstractCharacter] = set()
        self.spawn_handlers: Dict[AbstractCharacter, SpawnHandler] = {}
        self.teleporters = []
        self.base = None

    def add_character(self, character: AbstractCharacter):
        self.characters.add(character)
        self.add_spawn_handler(character)

    def remove_character(self, character:AbstractCharacter):
        self.characters.remove(character)

    def add_spawn_handler(self, character: AbstractCharacter):
        handler = SpawnHandler(
            char_instance=character,
            spawn_image=character.sprite.image,
            pixel_pos=self.get_spawn_icon_pos(),
            screen=character.screen
        )
        self.spawn_handlers[character] = handler

    def remove_spawn_handler(self, character: AbstractCharacter):
        del self.spawn_handlers[character]
        for handler in self.spawn_handlers.values():
            handler

    def get_spawn_icon_pos(self):
        n_prev_characters = len(self.characters)
        y = 110 + (n_prev_characters * 200)
        return (110, y)

    def set_main_base(self, base):
        self.main_base = base