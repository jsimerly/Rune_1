import pygame as pg
from typing import Type, List
from abc import ABC, abstractmethod

class ArchetypeInfoBase:
    icon_size = (100, 100)
    def __init__(self, icon_path:str, archetype_name: str) -> None:
        icon_path = icon_path
        image = pg.image.load(icon_path)
        self.image = pg.transform.scale(image, self.icon_size)
        self.name = archetype_name
        pg.font.init()
        self.font = pg.font.SysFont(None, 40)

    def draw(self, display: pg.Surface, pos:(int,int)):
        display.blit(self.image, pos)
        text_pos = (pos[0], pos[1] + 105)
        self.draw_text(display=display, pos=text_pos)

    def draw_text(self, display: pg.Surface, pos:(int,int)):
        text_surface = self.font.render(self.name, True, (255, 255, 255))
        display.blit(text_surface, pos)

tank_archetype = ArchetypeInfoBase('draft/gui/arch_type_icons/tank_logo.webp', 'Tank')
damage_archetype = ArchetypeInfoBase('draft/gui/arch_type_icons/damage_logo.webp', 'Damage')
#should add jungle here
support_archetype = ArchetypeInfoBase('draft/gui/arch_type_icons/support_logo.webp', 'Support')

class CharacterPreview:
    def __init__(self, position: (int, int),
        name: str, image_path: str, archetype: ArchetypeInfoBase,
        survivability: int, damage: int, utility: int, difficulty: int,
        abilities=[]   
    ) -> None:
        image_size = (400, 400)
        image = pg.image.load(image_path)
        self.name= name
        self.image = pg.transform.scale(image, image_size)
        self.archetype = archetype
        self.position = position
        self.survivability = survivability
        self.damage = damage
        self.utility = utility
        self.difficulty = difficulty
        self.abilities = abilities

        self.font = pg.font.SysFont(None, 28)
        self.character_font = pg.font.SysFont(None, 40)

    def draw(self, display: pg.Surface):
        self.draw_image(display)
        self.draw_name(display)
        x_pos = 810
        y_pos = self.position[1]
        y_pos += 280 # padding and 400 for image height
        self.draw_survivability(display=display, pos=(x_pos,y_pos))
        self.draw_damage(display=display, pos=(x_pos, y_pos + 30))
        self.draw_utility(display=display, pos=(x_pos, y_pos + 60))
        self.draw_difficulty(display=display, pos=(x_pos, y_pos + 90))

        archetype_pos = (x_pos + 425, y_pos)
        self.archetype.draw(display=display, pos=archetype_pos)

    def draw_image(self, display: pg.Surface):
        display.blit(self.image, self.position)

    def draw_name(self, display: pg.Surface):
        text_surface = self.character_font.render(self.name, True, (255, 255, 255))
        x_pos = self.position[0] + 400 + 300
        y_pos = self.position[1]
        text_pos = (x_pos, y_pos)
        display.blit(text_surface, text_pos)

    def draw_info_type(self, display: pg.Surface, 
        pos:(int,int), name: str, value: int, color: (int, int, int),
    ):
        if value > 10 or value <= 0:
            raise ValueError('value needs to be greater than 0 and less than 11')
        
        width = 90 + 30 * value
        size = (width, 25) #calculate this based on value
        rect = pg.Rect(pos, size)
        pg.draw.rect(display, color, rect, 0, 5)

        text_surface = self.font.render(name, True, (255, 255, 255))
        point = rect.topleft
        text_pos = (point[0] + 10, point[1] + 2)
        display.blit(text_surface, text_pos)

    def draw_survivability(self, display: pg.Surface, pos):
        self.draw_info_type(
            display= display, pos=pos,
            name = 'Durability',
            value = self.survivability,
            color = (1, 77, 2)
        )

    def draw_damage(self, display: pg.Surface, pos):
        self.draw_info_type(
            display= display, pos=pos,
            name = 'Damage',
            value = self.damage,
            color = (115, 11, 0)
        )

    def draw_utility(self, display: pg.Surface, pos):
        self.draw_info_type(
            display= display, pos=pos,
            name = 'Utility',
            value = self.utility,
            color = (100, 2, 115)
        )

    def draw_difficulty(self, display: pg.Surface, pos):
        self.draw_info_type(
            display= display, pos=pos,
            name = 'Difficulty',
            value = self.difficulty,
            color = (149, 220, 252)
        )


class AthleaPreview(CharacterPreview):
    def __init__(self, position: (int, int)) -> None:
        super().__init__(
            position, 
            name='Athlea',
            image_path='draft/gui/full_images/athlea.png',
            archetype=damage_archetype,
            survivability=5, 
            damage=3, 
            utility=8, 
            difficulty=3, 
            abilities=[]
        )

class BiziPreview(CharacterPreview):
    def __init__(self, position: (int, int)) -> None:
        super().__init__(
            position, 
            name='Bizi',
            image_path='draft/gui/full_images/bizi.png',
            archetype=support_archetype,
            survivability=4, 
            damage=5, 
            utility=8, 
            difficulty=8, 
            abilities=[]
        )

class BolindaPreview(CharacterPreview):
    def __init__(self, position: (int, int)) -> None:
        super().__init__(
            position, 
            name='Bolinda', 
            image_path='draft/gui/full_images/bolinda.png',
            archetype=damage_archetype,
            survivability=5, 
            damage=8, 
            utility=3, 
            difficulty=7, 
            abilities=[]
        )

class CrudPreview(CharacterPreview):
    def __init__(self, position: (int, int)) -> None:
        super().__init__(
            position, 
            name='Crud', 
            image_path='draft/gui/full_images/crud.png',
            archetype=tank_archetype,
            survivability=8, 
            damage=7, 
            utility=3, 
            difficulty=3, 
            abilities=[]
        )

class EmilyPreview(CharacterPreview):
    def __init__(self, position: (int, int)) -> None:
        super().__init__(
            position,  
            name='Emily',
            image_path='draft/gui/full_images/emily.png',
            archetype=support_archetype,
            survivability=6, 
            damage=2, 
            utility=10, 
            difficulty=3, 
            abilities=[]
        )

class HercPreview(CharacterPreview):
    def __init__(self, position: (int, int)) -> None:
        super().__init__(
            position,  
            name='Herc',
            image_path='draft/gui/full_images/herc.png',
            archetype=tank_archetype,
            survivability=9, 
            damage=6, 
            utility=2, 
            difficulty=5, 
            abilities=[]
        )

class IvanPreview(CharacterPreview):
    def __init__(self, position: (int, int)) -> None:
        super().__init__(
            position,  
            name='Ivan',
            image_path='draft/gui/full_images/ivan.png',
            archetype=damage_archetype,
            survivability=5, 
            damage=8, 
            utility=6, 
            difficulty=6, 
            abilities=[]
        )

class JudyPreview(CharacterPreview):
    def __init__(self, position: (int, int)) -> None:
        super().__init__(
            position,  
            name='Judy',
            image_path='draft/gui/full_images/judy.png',
            archetype=damage_archetype,
            survivability=3, 
            damage=8, 
            utility=6, 
            difficulty=4, 
            abilities=[]
        )

class KanePreview(CharacterPreview):
    def __init__(self, position: (int, int)) -> None:
        super().__init__(
            position,  
            name='Kane',
            image_path='draft/gui/full_images/kane.png',
            archetype=tank_archetype,
            survivability=10, 
            damage=3, 
            utility=8, 
            difficulty=3, 
            abilities=[]
        )

class LuPreview(CharacterPreview):
    def __init__(self, position: (int, int)) -> None:
        super().__init__(
            position,  
            name='Lu',
            image_path='draft/gui/full_images/lu.png',
            archetype=damage_archetype,
            survivability=7, 
            damage=7, 
            utility=7, 
            difficulty=7, 
            abilities=[]
        )

class NaviPreview(CharacterPreview):
    def __init__(self, position: (int, int)) -> None:
        super().__init__(
            position,  
            name='Navi',
            image_path='draft/gui/full_images/navi.png',
            archetype=damage_archetype,
            survivability=7, 
            damage=5, 
            utility=8, 
            difficulty=9, 
            abilities=[]
        )

class PapaPreview(CharacterPreview):
    def __init__(self, position: (int, int)) -> None:
        super().__init__(
            position, 
            name='Papa', 
            image_path='draft/gui/full_images/papa.png',
            archetype=damage_archetype,
            survivability=5, 
            damage=5, 
            utility=5, 
            difficulty=5, 
            abilities=[]
        )

class TimPreview(CharacterPreview):
    def __init__(self, position: (int, int)) -> None:
        super().__init__(
            position,  
            name='Tim',
            image_path='draft/gui/full_images/tim.png',
            archetype=damage_archetype,
            survivability=1, 
            damage=10, 
            utility=3, 
            difficulty=10, 
            abilities=[]
        )

draft_previews: List[Type[CharacterPreview]] = [
    AthleaPreview,
    BiziPreview,
    BolindaPreview,
    CrudPreview,
    EmilyPreview,
    HercPreview,
    IvanPreview,
    JudyPreview,
    KanePreview,
    LuPreview,
    NaviPreview,
    PapaPreview,
    TimPreview,
]