from __future__ import annotations
from typing import TYPE_CHECKING, List, Callable
from time import sleep



#highly coupled with GameManager, really just a 1 to 1 extension
class TurnManager:
    def __init__(self, t1_game_manager: GameManager):
        self.t1_game_manager = t1_game_manager
        self.t1_is_ended = False
        self.start_of_turn_events: List[Callable]  = []
        self.end_of_turn_events: List[Callable] = []


    def check_for_end(self):
        return self.t1_game_manager.turn_ended
        #will eventually check for both teams

    def start_of_turn(self):
        for func in self.start_of_turn_events:
            func()

    def end_of_turn(self):
        for func in self.end_of_turn_events:
            func()

    '''Team Management'''
    def team_1_end_turn(self):
        self.t1_is_ended = True
        turn_ended = self.check_for_end()
        if turn_ended:
            self.handle_end_of_turn()
            # Start of Turn 
            # Movement
                # Picking Up Shards
                # Melee Abilities
                # Walkthrough Effects
            # Abilities
                # Damage
                # Healing / Shielding
            # Other
                # Misc Player Movement
                # Altar Process
                # Rune Processing
                # Respawn Handling
            #Turn over

            self.leveling()

    '''Start of Turn'''

    '''End of Turn'''
    def handle_end_of_turn(self):
        self.movement()
        self.leveling()

    ''' Movement '''
    def movement(self):
        processing_movement = True
        while processing_movement:
            some_moves_left = False
            index = 0
            for character in self.t1_game_manager.team.characters:
                moves_left = character.process_next_move()
                
                if moves_left:
                    some_moves_left = True

            if not some_moves_left:
                break
            
            sleep(0.25)
            if index > 20:
                break
            index += 1

    def leveling(self):
        for rune in self.t1_game_manager.leveling_stones:
            rune.on_end_of_turn()

    '''Registering Events'''
    def register_start_event(self, event: Callable):
        self.start_of_turn_events.append(event)

    def unregister_start_event(self, event: Callable):
        self.start_of_turn_events.remove(event)

    def register_end_event(self, event: Callable):
        self.end_of_turn_events.append(event)

    def unregister_end_event(self, event: Callable):
        self.end_of_turn_events.remove(event)