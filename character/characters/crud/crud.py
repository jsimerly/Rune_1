from character.abs_character import AbstractCharacter
from components.sprite import SpriteComponent
from components.movement import MovementComponent

#Crud builder
class Crud(AbstractCharacter):
    def __init__(self, surface):
        super().__init__(surface)
        image = self.open_image('character/characters/crud/gui/crud.png')
        
        self.set_sprite_comp(image)
        self.set_movement_comp()
        self.set_color((186, 17, 17))




    