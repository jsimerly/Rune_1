from character.abs_character import AbstractCharacter
from components.sprite import SpriteComponent

#Crud builder
class Crud(AbstractCharacter):
    def __init__(self, screen):
        super().__init__(screen)
        image = self.open_image('character/characters/crud/gui/crud.png')
        
        sprite_comp = SpriteComponent(image, self.screen)
        self.set_sprite_comp(sprite_comp)





    