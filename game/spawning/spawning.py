from ui.spawning_icon import CharacterSpawningIcon


# Later attach to team to handle many characters.
class SpawnHandler:
    def __init__(self, char_instance, spawn_image, pixel_pos, screen) -> None:
        self.character = char_instance
        self.button = CharacterSpawningIcon(spawn_image, pixel_pos, screen, char_instance=char_instance)
        self.draw()

    def draw(self):
        #loop through teams characters buttons and draw
        self.button.draw()
