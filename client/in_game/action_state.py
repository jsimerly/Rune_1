from enum import Enum, auto
from in_game.event_bus import EventBus
class ActionState(Enum):
    IDLE = auto()
    SPAWNING = auto()
    TILE_SELECTED = auto()
    CHARACTER_SELECTED = auto()
    CHARACTER_ABILITY = auto()
    TURN_ENDED = auto()
class ActionStateManager:
    def __init__(self, event_bus: EventBus) -> None:
        self.current_state = ActionState.IDLE
        self.event_bus = event_bus
        self.event_bus.subscribe('spawning_started', self.spawning)
        self.event_bus.subscribe('spawn_to_tile', self.idle)
        self.event_bus.subscribe('character_selected', self.character_selected)
        # self.event_bus.subscribe('entity_moved_to_tile', self.idle)

    @property
    def is_idle(self):
        return self.current_state == ActionState.IDLE

    @property
    def is_spawning(self):
        return self.current_state == ActionState.SPAWNING
    
    @property
    def is_tile_selected(self):
        return self.current_state == ActionState.TILE_SELECTED
    
    @property
    def is_character_selected(self):
        return self.current_state == ActionState.CHARACTER_SELECTED
    
    @property
    def is_ability_selected(self):
        return self.current_state == ActionState.CHARACTER_ABILITY
    
    @property
    def is_turn_ended(self):
        return self.current_state == ActionState.TURN_ENDED
    

    def idle(self, **kwargs):
        self.switch_state(ActionState.IDLE)

    def spawning(self, **kwargs):
        self.switch_state(ActionState.SPAWNING)

    def character_selected(self, **kwargs):
        self.switch_state(ActionState.CHARACTER_SELECTED)

    def character_ability(self, **kwargs):
        self.switch_state(ActionState.CHARACTER_ABILITY)

    def turn_ended(self, **kwargs):
        self.switch_state(ActionState.TURN_ENDED)

    def switch_state(self, new_state: ActionState):
        self.on_state_exit(self.current_state)
        self.current_state = new_state
        self.on_state_enter(self.current_state)

    def on_state_exit(self, state: ActionState):
        exit_event = f'{state.name.lower()}_exit'
        self.event_bus.publish(exit_event)

    def on_state_enter(self, state: ActionState):
        enter_event = f'{state.name.lower()}_enter'
        print(enter_event)
        self.event_bus.publish(enter_event)


    