from __future__ import annotations
from typing import Protocol, Tuple, Dict, Set, List, TYPE_CHECKING
from abc import ABC
from map.game_tile import GameTile
from client.in_game.surfaces import GameSurfaces
from character.abs_character import AbstractCharacter
from zclient.ui.buttons.button import Button, ButtonManager
from zclient.ui.buttons.ability_button import AbilityButton
from zclient.ui.buttons.spawn_button import SpawnButton
from zclient.ui.buttons.end_turn_button import EndTurnButton
from zclient.ui.buttons.button import Button

if TYPE_CHECKING:
    from client.in_game.game_manager import GameManager

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
        self.option_tiles: List[GameTile] = None
        self.character: AbstractCharacter = None
        self.ability = None

    def clear(self):
        self.ui_obj = None
        self.tile = None
        self.option_tiles: List[GameTile] = None
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
                self.context.tile = obj
                self.context.character = obj.ghost_character

                if obj.character and obj.ghost_character:
                    return CharacterSelectedState
                
                if obj.character:
                    self.context.character = obj.character
                    print('ability selection')
                    return None
                
                if obj.ghost_character:
                    return CharacterSelectedState
                
                return IdleState
            
            if isinstance(obj, SpawnButton):
                self.context.character = obj.character
                self.context.ui_obj = obj
                obj.on_click()
                return SpawningState_Click
            
            if isinstance(obj, AbilityButton):
                return AbilityState_Click
            
            if isinstance(obj, EndTurnButton):
                self.game_manager.end_turn()
                return IdleState
            
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
        self.spawn_options: List[GameTile] = []

    def input(self, input: MouseInput) -> ActionState:
        obj = self.game_manager.find_interactable_obj(input.pixel)
        if not obj:
            return IdleState
        
        if isinstance(input, Click):
            if isinstance(obj, GameTile):
                placed = self._spawn_character(obj)
                if placed:
                    return IdleState
                return None
            
            if isinstance(obj, SpawnButton):
                self.context.ui_obj.deselect()
                if obj == self.context.ui_obj:
                    return IdleState
                
                self.context.ui_obj = obj
                self.context.character = obj.character
                return SpawningState_Click
            
        if isinstance(input, DragEnd):
            if isinstance(obj, GameTile):
                placed = self._spawn_character(obj)
                if placed:
                    return IdleState
                return None

    def update(self, mouse_pos) -> ActionState:
        ...

    def on_enter(self):
        character = self.context.character
        if not character and not isinstance(character, AbstractCharacter):
            raise ValueError('There was is no character assigned to this button. Please check the action_context to make sure a character is assigned.')
        self.character = character

        if self.character.current_tile:
            self.character.clear_move()
            self.character.remove_from_tile()
            self.character.sprite.remove_ghost()

        self.spawn_options = self.character.team.get_spawnable_tiles()
        for tile in self.spawn_options:
            tile.set_option()
 
        self.context.ui_obj.select()
        
    def on_exit(self):
        for tile in self.spawn_options:
            tile.remove_option()

    def _spawn_character(self, obj: GameTile) -> bool:
        if not obj.map_interaction.can_end_on:
            print("Cannot spawn your character there as something else is already in the way.")
            return False
        
        if obj not in self.spawn_options:
            print("You need to spawn the character inside of a teleporter's range.")
            return False


        obj.spawn_character(self.context.character)
        self.context.ui_obj.deselect()
        return True

class CharacterMoveSelected(ActionState):
    def __init__(self, game_manager) -> None:
        self.game_manager: GameManager = game_manager
        self.context = self.game_manager.action_context
        self.move_options: List[GameTile] = []

    def input(self, input: MouseInput) -> ActionState:
        obj = self.game_manager.find_interactable_obj(input.pixel)
        if not obj:
            return IdleState
        
        if isinstance(obj, GameTile):
            if isinstance(input, Click):
                if obj in self.move_options:
                    print('in move options')
                    self.character.move_to_tile(obj)
                return IdleState
            
        if isinstance(input, DragStart):
            self.character.drag_move_start()
            
        if isinstance(input, DragEnd):
            if obj in self.move_options:
                self.character.drag_move_finish(obj)
            return IdleState
            #check if we finished on a tile if not clear the queue

        #if an ability icon then we attack!
        return None
            
    def update(self, mouse_pos):
        obj = self.game_manager.find_interactable_obj(mouse_pos)
        if not obj:
            return None
        
        if isinstance(obj, GameTile):
            self.character.drag_move(obj)

    def on_enter(self):
        if not self.context.character:
            raise ValueError("action_context needs to have a character assigned to etner Character Selected State.")
        
        if not self.context.tile:
            raise ValueError("action_context needs to have a tile assigned to enter Character Selected State.")
        
        self.character = self.context.character
        self.tile = self.context.tile

        #Open up ability ui

        self.move_options = self.character.movement.find_possible_tiles(self.tile)
        for tile in self.move_options:
            tile.set_option()
        self.tile.select()
    
    def on_exit(self):
        for tile in self.move_options:
            tile.remove_option()
        self.tile.deselect()

class CharacterSelectedState(ActionState):
    def __init__(self, game_manager) -> None:
        self.game_manager: GameManager = game_manager
        self.context = self.game_manager.action_context
        self.move_options: List[GameTile] = []

    def input(self, input: MouseInput) -> ActionState:
        obj = self.game_manager.find_interactable_obj(input.pixel)
        if not obj:
            return IdleState
        
        if isinstance(obj, GameTile):
            if isinstance(input, Click):
                if obj in self.move_options:
                    self.character.move_to_tile(obj)
                else:
                    print('You cannot move there.')
                return IdleState
            
        if isinstance(input, DragStart):
            self.character.drag_move_start()
            
        if isinstance(input, DragEnd):
            if obj in self.move_options:
                self.character.drag_move_finish(obj)
            else:
                print('You cannot move there.')
            return IdleState
            #check if we finished on a tile if not clear the queue

        #if an ability icon then we attack!
            
    def update(self, mouse_pos):
        obj = self.game_manager.find_interactable_obj(mouse_pos)
        if not obj:
            return None
        
        if isinstance(obj, GameTile):
            self.character.drag_move(obj)

    def on_enter(self):
        if not self.context.character:
            raise ValueError("action_context needs to have a character assigned to etner Character Selected State.")
        
        if not self.context.tile:
            raise ValueError("action_context needs to have a tile assigned to enter Character Selected State.")
        
        self.character = self.context.character
        self.tile = self.context.tile

        #Open up ability ui

        self.move_options = self.character.movement.find_possible_tiles(self.tile)
        for tile in self.move_options:
            tile.set_option()
        self.tile.select()
    
    def on_exit(self):
        for tile in self.move_options:
            tile.remove_option()
        self.tile.deselect()

class EmptyTileSelected(ActionState):
    pass


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
