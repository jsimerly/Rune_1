from enum import Enum
from game.ui.phase_buttons import  PhaseButton
from game.phases.abstact_phase_manager import AbstactPhaseManager
import pygame as pg
from settings import BGCOLOR


class GamePhase(Enum):
    SPAWNING = 1
    MOVE_QUEUEING = 2
    ABILITY_QUEUEING = 3
    TURN_ENDED = 4

class GamePhaseManager:
    def __init__(self, screen):
        self.screen = screen
        self.current_phase = GamePhase.SPAWNING
        self.turn_n = 0

        self.next_phase_button = PhaseButton(
            screen=screen, pixel_pos=(190, 900),
            text='Next', color=(255, 255, 255), border_color=(100, 100, 100),
            on_click=self.next_phase
        )
        self.prev_phase_button = PhaseButton(
            screen=screen, pixel_pos=(30, 900),
            text='Prev', color=(255, 255, 255), border_color=(100, 100, 100),
            on_click=self.prev_phase
        )

        self.spawn_handler = None
        self.move_handler = None
        self.ability_handler = None
        self.processing_handler = None
        self.draw()

    def set_phase(self, phase: AbstactPhaseManager):
        self.current_phase = phase
        self.draw_current_phase_text()

    def next_phase(self):
        next_phase = GamePhase((self.current_phase.value % len(GamePhase)) + 1)
        self.set_phase(next_phase)

    def prev_phase(self):
        next_phase = GamePhase((self.current_phase.value % len(GamePhase)) + 1)
        self.set_phase(next_phase)

    def is_phase(self, phase: GamePhase):
        return self.current_phase == phase
    
    def draw_current_phase_text(self):
        text_map = {
            GamePhase.SPAWNING: 'Spawning',
            GamePhase.MOVE_QUEUEING: 'Movement',
            GamePhase.ABILITY_QUEUEING: 'Abilities',
            GamePhase.TURN_ENDED: 'Waiting on Other Player'
        }

        text = text_map[self.current_phase]
        font = pg.font.SysFont('Arial', 24)
        text_surf = font.render(text, True, (255, 255, 255))
        fill_rect = pg.Rect(33, 952, 270, 50)
        self.screen.fill(BGCOLOR, fill_rect)
        self.screen.blit(text_surf, (33, 952))

    
    def draw(self):
        self.draw_current_phase_text()
        self.next_phase_button.draw()
        self.prev_phase_button.draw()

    
# Move Between Phases
    
# Later attach to team to handle many characters.






