from __future__ import annotations
from typing import TYPE_CHECKING, List, Set, Dict
from character.abs_character import AbstractCharacter
from game.phases.spawn_handler import SpawnHandler
from game.game_phase import GamePhase, GamePhaseManager

class Team:
    def __init__(self, team_id, screen):
        self.team_id = team_id
        self.color: (int, int, int) = (0,0,0)
        self.max_team_size:int = 3
        self.screen = screen

        self.characters: Set[AbstractCharacter] = set()
        self.spawn_handlers: Dict[AbstractCharacter, SpawnHandler] = {}
        self.game_phase_manager: GamePhaseManager = GamePhaseManager(screen=screen)
        self.teleporters = []
        self.base = None

    def add_character(self, character: AbstractCharacter):
        if len(self.characters) >= self.max_team_size:
            print(f'Team at max size of {self.max_team_size}.')
            return
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
        y = n_prev_characters * 200
        return (110, y)

    def set_main_base(self, base):
        self.main_base = base