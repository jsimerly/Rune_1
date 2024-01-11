from __future__ import annotations
from typing import Protocol, Tuple, Dict, Set, List
from map.game_tile import GameTile
from surfaces import Surfaces
from character.abs_character import AbstractCharacter
from ui.buttons.button import Button, ButtonManager
from ui.buttons.ability_button import AbilityButton
from ui.buttons.spawn_button import SpawnButton
from ui.buttons.end_turn_button import EndTurnButton
from hex import Layout

class ActionState(Protocol):
    def on_enter(self):
        ...

    def on_exit(self):
        ...

    def input(self, event) -> ActionState:
        ...

    def update(self, event) -> ActionState:
        ...


class MouseInput(Protocol):
    ...

class ClickAction(MouseInput):
    def __init__(self, obj) -> None:
        self.obj = obj

class DragAction(MouseInput):
    def __init__(self, obj) -> None:
        self.start_obj = obj
        self.current_obj = obj

    def update_mouse_pos(self, obj):
        self.current_obj = obj

class InteractableObject:
    ...

class ClickabeObj(InteractableObject):
    ...

class DraggableObj(InteractableObject):
    ...

class GameManagerContext(Protocol):
    button_manager: ButtonManager
    surfaces: Surfaces
    layout: Layout

    tiles: Dict[Tuple[int,int], GameTile]
    characters: List[AbstractCharacter]
    buildings = []
    enemy_characters: List[AbstractCharacter]
    enemy_buildings = []

    leveling_stones = []
    leveling_shards = []
    altars = []

    is_dragging: bool
    action_state: ActionState

    def set_state(self, state: ActionState) -> None:
        ...

    def input(self) -> None:
        ...

    def update(self) -> None:
        ...
    
    

class IdleState(ActionState):
    def input(self, input: MouseInput) -> ActionState:
        #Click
        if isinstance(input, ClickAction):
            if isinstance(input.obj, GameTile):
                if input.obj.character:
                    return MovementState_Click()
                return IdleState()
            
            if isinstance(input.obj, SpawnButton):
                return SpawningState_Click()
            
            if isinstance(input.obj, AbilityButton):
                return AbilityState_Click()
            
            if isinstance(input.obj, EndTurnButton):
                return TurnEndedState()
            
        #Drag
        if isinstance(input, DragAction):
            if isinstance(input.start_obj, GameTile):
                if input.start_obj.character and input.start_obj.character.movement.queue.is_empty:
                    return SpawningState_Drag()
                
                if input.start_obj.character:
                    return MovementState_Drag()
                
                if input.start_obj.ghost_character:
                    return SpawningState_Drag()
                return IdleState()
                        
        return IdleState()


class SpawningState_Click(ActionState):
    pass

class SpawningState_Drag(ActionState):
    pass

class MovementState_Click(ActionState):
    pass

class MovementState_Drag(ActionState):
    pass

class AbilityState_Click(ActionState):
    pass

class AbilityState_Drag(ActionState):
    pass

class TurnEndedState(ActionState):
    pass



