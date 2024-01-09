from game.ui.spawning_icon import CharacterSpawningIcon
from .abstact_phase_manager import AbstactPhaseManager

class SpawnHandler(AbstactPhaseManager):
    def __init__(self, char_instance, spawn_image, pixel_pos, screen) -> None:
        self.character = char_instance
        self.button = CharacterSpawningIcon(spawn_image, pixel_pos, screen, char_instance=char_instance)
        self.draw()

    def draw(self):
        #loop through teams characters buttons and draw
        self.button.draw()

    def move_pos(self):
        self.button.pos