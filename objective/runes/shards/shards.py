from __future__ import annotations
from objective.abs_objective import AbstactObjective
from components.map_interaction import MapInteractionComponent
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from map.game_tile import GameTile
    import pygame as pg
    from character.abs_character import AbstractCharacter


class RuneShards(AbstactObjective):
    def __init__(self,   
        tile: GameTile,
        respawn_rate:int, 
        power: int,
        image_path:str, 
        spawn_turn: int = 0
    ) -> None:
        super().__init__(spawn_turn)

        self.tile = tile
        self.respawn_rate = respawn_rate
        self.turns_until_respawn = respawn_rate
        self.is_active = True
        self.power = power

        image = self.open_image(image_path)
        self.set_sprite_comp(image)
        self.sprite.move_to_tile(self.tile)
        self.map_interatcions = MapInteractionComponent(
            is_passable=True,
            can_pierce=True,
            can_end_on=True,
            blocks_vision=False,
            hides_occupants=False,
            is_slowing=False,
            walkthrough_effects=self.walkthough_effect
        )

    def walkthough_effect(self, character: AbstractCharacter):
        if self.is_active:
            character.leveling.add_pp(self.power)
            self.is_active = False

    def on_end_of_turn(self):
        super().on_end_of_turn()
        if not self.is_active:

            self.turns_until_respawn -= 1
            if self.turns_until_respawn == 0:
                self.is_active = True
                self.turns_until_respawn = self.respawn_rate

    def draw(self, screen: pg.Surface):
        if self.is_active:
            super().draw(screen)

        
