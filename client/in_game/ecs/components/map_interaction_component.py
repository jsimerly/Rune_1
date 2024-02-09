from in_game.ecs.components.component_base import Component
from dataclasses import dataclass


class TileMapInteractionComponent(Component):
    def __init__(self, blocks_los, is_passable, can_end_on, can_pierce, hides_occupants, is_slowing) -> None:
        self.blocks_los: bool  = blocks_los
        self.is_passable: bool = is_passable
        self.can_end_on: bool = can_end_on
        self.can_pierce: bool = can_pierce
        self.hides_occupants: bool = hides_occupants
        self.is_slowing:bool = is_slowing

        self.default_blocks_los: bool = self.blocks_los
        self.default_is_passable: bool = self.is_passable
        self.default_can_end_on: bool = self.can_end_on 
        self.default_can_pierce: bool = self.can_pierce
        self.default_hides_occupants: bool = self.hides_occupants
        self.default_is_slowing:bool = self.is_slowing

@dataclass
class MapInteractionComponent(Component):
    blocks_los: bool 
    is_passable: bool
    can_end_on: bool
    can_pierce: bool
    hides_occupants: bool
    is_slowing:bool
