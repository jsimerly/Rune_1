from .abstact_component import  AbstactComponent
from typing import Callable, TYPE_CHECKING, List
if TYPE_CHECKING:
    print()

class MapInteractionComponent(AbstactComponent):
    def __init__(self,
        is_passable, 
        can_pierce,
        can_end_on, 
        blocks_vision, 
        hides_occupants, 
        is_slowing,       
        walkthrough_effects
    ):

        self.is_passable = is_passable
        self.can_pierce = can_pierce
        self.can_end_on = can_end_on
        self.blocks_vision = blocks_vision
        self.hides_occupants = hides_occupants
        self.is_slowing = is_slowing
        
        self.default_is_passable = is_passable
        self.default_can_pierce = can_pierce
        self.default_can_end_on = can_end_on
        self.default_blocks_vision = blocks_vision
        self.default_hides_occupants = hides_occupants
        self.default_is_slowing = is_slowing
        self.walkthrough_effects: List[Callable] = walkthrough_effects


    def set_is_passable(self, value):
        self.is_passable = value

    def set_can_pierce(self, value):
        self.can_pierce = value

    def set_can_end_on(self, value):
        self.can_end_on = value

    def set_blocks_vision(self, value):
        self.blocks_vision = value

    def set_hides_occupants(self, value):
        self.hides_occupants = value

    def set_is_slowing(self, value):
        self.is_slowing = value

    def reset_is_passable(self):
        self.is_passable = self.default_is_passable

    def reset_can_pierce(self):
        self.can_pierce = self.default_can_pierce

    def reset_can_end_on(self):
        self.can_end_on = self.default_can_end_on

    def reset_blocks_vision(self):
        self.blocks_vision = self.default_blocks_vision
    
    def reset_hides_occupant(self):
        self.hides_occupants = self.default_hides_occupants

    def reset_is_slowing(self):
        self.is_slowing = self.default_is_slowing

    def trigger_walkthrough_effects(self, character):
        for effect in self.walkthrough_effects:
            #do effects 
            pass

    def add_walkthrough_effect(self, effect: Callable):
        self.walkthrough_effects.append(effect)

    def remove_walkthrough_effect(self, effect:Callable):
        if effect in self.walkthrough_effects:
            self.walkthrough_effects.remove(effect)

    @property
    def movement_cost(self):
        if self.is_slowing:
            return 2
        return 1