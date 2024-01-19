from character.abs_character import AbstractCharacter
from components.sprite import SpriteComponent
from components.movement import MovementComponent



class Emilie(AbstractCharacter):
    def __init__(self):
        image = self.open_image('character/characters/emilie/gui/emilie.webp')
        super().__init__(
            image=image,
            color=(228, 230, 149)
        )
