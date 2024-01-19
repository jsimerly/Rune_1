from character.abs_character import AbstractCharacter
from components.sprite import SpriteComponent
from components.movement import MovementComponent

#Crud builder
class Crud(AbstractCharacter):
    def __init__(self):
        image = self.open_image('character/characters/crud/gui/crud.png')
        super().__init__(
            image=image,
            color = (186, 17, 17)
        )
        





    