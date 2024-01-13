from character.abs_character import AbstractCharacter
from components.sprite import SpriteComponent
from components.movement import MovementComponent




class Emilie(AbstractCharacter):
    def __init__(self, surface):
        super().__init__(surface)
        image = self.open_image('character/characters/emilie/gui/emilie.webp')
        
        self.set_sprite_comp(image)
        self.set_movement_comp()
        self.set_color((228, 230, 149))