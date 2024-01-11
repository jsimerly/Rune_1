from __future__ import annotations
from typing import Protocol, Tuple, Dict, Set, List, TYPE_CHECKING
from abc import ABC
from map.game_tile import GameTile
from client.surfaces import GameSurfaces
from character.abs_character import AbstractCharacter
from client.ui.buttons.button import Button, ButtonManager
from client.ui.buttons.ability_button import AbilityButton
from client.ui.buttons.spawn_button import SpawnButton
from client.ui.buttons.end_turn_button import EndTurnButton
from client.ui.buttons.button import Button
from hex import Layout
if TYPE_CHECKING:
    from game_manager import GameManager

class ActionState(Protocol):
    def input(self, obj) -> ActionState:
        ...

    def update(self, obj) -> ActionState:
        ...

    def on_enter(self):
        ...

    def on_exit(self):
        ...


class MouseInput(ABC):
     def __init__(self, pixel) -> None:
        self.pixel = pixel
class Click(MouseInput):
    def __init__(self, pixel) -> None:
        self.pixel = pixel

class DragStart(MouseInput):
    def __init__(self, pixel) -> None:
        self.pixel = pixel

class DragEnd(MouseInput):
    def __init__(self, pixel) -> None:
        self.pixel = pixel


class InteractableObject:
    ...

class ClickabeObj(InteractableObject):
    ...

class DraggableObj(InteractableObject):
    ...
    

class ActionContext:
    def __init__(self):
        self.ui_obj: Button = None
        self.tile: GameTile = None
        self.character: AbstractCharacter = None
        self.ability = None

    def clear(self):
        self.ui_obj = None
        self.tile = None
        self.character = None
        self.ability = None

class IdleState(ActionState):
    def __init__(self, game_manager) -> None:
        self.game_manager: GameManager = game_manager
        self.context = self.game_manager.action_context
    
    def input(self, input: MouseInput) -> ActionState:
        obj = self.game_manager.find_interactable_obj(input.pixel)
        if not obj:
            return None
        
        #Click
        if isinstance(input, Click):
            if isinstance(obj, GameTile):
                if obj.character:
                    self.context.tile = obj
                    self.context.character = obj.character
                    return MovementState_Click
                return None
            
            if isinstance(obj, SpawnButton):
                if obj.character.current_tile:
                    obj.character.remove_from_tile()

                self.context.ui_obj = obj
                obj.on_click()
                return SpawningState_Click
            
            if isinstance(obj, AbilityButton):
                return AbilityState_Click
            
            if isinstance(obj, EndTurnButton):
                return TurnEndedState
            
        #Drag
        if isinstance(input, DragStart):
            if isinstance(obj, GameTile):
                if obj.character and obj.character.movement.queue.is_empty:
                    return SpawningState_Drag
                
                if obj.character:
                    return MovementState_Drag
                
                if obj.ghost_character:
                    return SpawningState_Drag
                return None
            
            if isinstance(obj, SpawnButton):
                return SpawningState_Drag
                        
        return None
    
    def update(self, mouse_pos: Tuple[int, int]):
        #Could use this to show hover actions. We won't as we're thinking mobile focused.
        pass

    def on_enter(self):
        self.game_manager.action_context.clear()


class SpawningState_Click(ActionState):
    def __init__(self, game_manager) -> None:
        self.game_manager: GameManager = game_manager
        self.context = self.game_manager.action_context

    def input(self, input: MouseInput) -> ActionState:
        obj = self.game_manager.find_interactable_obj(input.pixel)
        if not obj:
            return IdleState
        
        if isinstance(input, Click):
            if isinstance(obj, GameTile):
                #check if we can spawn here
                obj.character = self.character
                obj.character.sprite.draw(obj.center_pixel)
                self.context.ui_obj.on_click()

                return IdleState
            
            if isinstance(obj, SpawnButton):
                obj.on_click()
                if obj != self.game_manager.action_context.ui_obj:
                    self.context.ui_obj.on_click()

                self.context.ui_obj = obj
                return SpawningState_Click


    def update(self, mouse_pos) -> ActionState:
        ...

    def on_enter(self):
        character = self.context.ui_obj.character
        if not character and not isinstance(character, AbstractCharacter):
            raise ValueError('There was is no character assigned to this button. Please check the action_context to make sure a character is assigned.')
        
        self.character = character
        

class MovementState_Click(ActionState):
    pass

class AbilityState_Click(ActionState):
    pass

class MovementState_Drag(ActionState):
    pass

class SpawningState_Drag(ActionState):
    pass

class AbilityState_Drag(ActionState):
    pass

class TurnEndedState(ActionState):
    pass
