from character.abs_character import AbstractCharacter
from components.sprite import SpriteComponent
from components.movement import MovementComponent

#Crud builder
class Emilie(AbstractCharacter):
    def __init__(self, surface):
        super().__init__(surface)
        image = self.open_image('character/characters/emilie/gui/emilie.webp')
        
        sprite_comp = SpriteComponent(image, self.surface)
        move_comp = MovementComponent(character=self)
        self.set_sprite_comp(sprite_comp)
        self.set_movement_comp(move_comp)
        self.set_color((228, 230, 149))