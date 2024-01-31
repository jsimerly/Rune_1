import pygame as pg


class CharacterPreview:
    def __init__(self, 
        name:str, image: pg.Surface, 
        durability: int, damage: int, utility: int, difficulity: int, 
        abilitites=[]
    ) -> None:
        self.name=name
        self.image=image
        self.durability=durability
        self.damage=damage
        self.utility=utility
        self.difficulty=difficulity
        #figure out abilities later.


class DraftCharacter:
    def __init__(self, 
            name: str, 
            server_name: str, 
            icon_image: pg.Surface, 
            preview_image: pg.Surface,
            durability: int,
            damage: int,
            utility: int,
            difficulty: int,
            abilities = [],
        ) -> None:

        if 0 >= durability > 10:
            raise ('durability of each character needs to be between 1-10.')
        if 0 >= damage > 10:
            raise ('damage of each character needs to be between 1-10.')
        if 0 >= utility > 10:
            raise ('utility of each character needs to be between 1-10.')
        if 0 >= difficulty > 10:
            raise ('difficulty of each character needs to be between 1-10.')
        

        preview_image = pg.image.load(preview_image)
        preview_image = pg.transform.scale(preview_image, (400, 400))
        self.preview = CharacterPreview(
            name, preview_image, 
            durability=durability, damage=damage, difficulity=difficulty, utility=utility,
            abilitites=abilities
        )

        self.name = name
        self.server_name = server_name
        icon_image = pg.image.load(icon_image)
        self.icon_image = pg.transform.scale(icon_image, (150, 150))

        self.is_picked = False
        self.is_banned = False
        self.is_banning = False
        self.is_selected = False

class Athlea_DraftCharacter(DraftCharacter):
    def __init__(self):
        super().__init__(
            name='Athlea', server_name='athlea',
            icon_image='draft/gui/icon_images/athlea_icon.png',
            preview_image='draft/gui/full_images/athlea.png',
            durability=5,
            damage=3,
            utility=8,
            difficulty=3
        )

class Bizi_DraftCharacter(DraftCharacter):
    def __init__(self):
        super().__init__(
            'Bizi', 'bizi',
            icon_image='draft/gui/icon_images/bizi_icon.png',
            preview_image='draft/gui/full_images/bizi.png',
            durability=4,
            damage=5,
            utility=8,
            difficulty=8
        )

class Bolinda_DraftCharacter(DraftCharacter):
    def __init__(self):
        super().__init__(
            'Bolinda', 'bolinda',
            icon_image='draft/gui/icon_images/bolinda_icon.png',
            preview_image='draft/gui/full_images/bolinda.png',
            durability=5,
            damage=8,
            utility=3,
            difficulty=7
        )

class Crud_DraftCharacter(DraftCharacter):
    def __init__(self):
        super().__init__(
            'Crud', 'crud',
            icon_image='draft/gui/icon_images/crud_icon.png',
            preview_image='draft/gui/full_images/crud.png',
            durability=8,
            damage=7,
            utility=3,
            difficulty=3
        )

class Emily_DraftCharacter(DraftCharacter):
    def __init__(self):
        super().__init__(
            'Emily', 'emily',
            icon_image='draft/gui/icon_images/emily_icon.png',
            preview_image='draft/gui/full_images/emily.png',
            durability=6,
            damage=2,
            utility=10,
            difficulty=3
        )

class Herc_DraftCharacter(DraftCharacter):
    def __init__(self):
        super().__init__(
            'Herc', 'herc',
            icon_image='draft/gui/icon_images/herc_icon.png',
            preview_image='draft/gui/full_images/herc.png',
            durability=9,
            damage=6,
            utility=2,
            difficulty=5
        )

class Ivan_DraftCharacter(DraftCharacter):
    def __init__(self):
        super().__init__(
            'Ivan', 'ivan',
            icon_image='draft/gui/icon_images/ivan_icon.png',
            preview_image='draft/gui/full_images/ivan.png',
            durability=5,
            damage=8,
            utility=6,
            difficulty=6
        )

class Judy_DraftCharacter(DraftCharacter):
    def __init__(self):
        super().__init__(
            'Judy', 'judy',
            icon_image='draft/gui/icon_images/judy_icon.png',
            preview_image='draft/gui/full_images/judy.png',
            durability=3,
            damage=8,
            utility=6,
            difficulty=4
        )

class Kane_DraftCharacter(DraftCharacter):
    def __init__(self):
        super().__init__(
            'Kane', 'kane',
            icon_image='draft/gui/icon_images/kane_icon.png',
            preview_image='draft/gui/full_images/kane.png',
            durability=10,
            damage=3,
            utility=8,
            difficulty=3
        )

class Lu_DraftCharacter(DraftCharacter):
    def __init__(self):
        super().__init__(
            'Lu', 'lu',
            icon_image='draft/gui/icon_images/lu_icon.png',
            preview_image='draft/gui/full_images/lu.png',
            durability=7,
            damage=7,
            utility=3,
            difficulty=7
        )

class Navi_DraftCharacter(DraftCharacter):
    def __init__(self):
        super().__init__(
            'Navi', 'navi',
            icon_image='draft/gui/icon_images/navi_icon.png',
            preview_image='draft/gui/full_images/navi.png',
            durability=7,
            damage=5,
            utility=8,
            difficulty=9
        )

class Papa_DraftCharacter(DraftCharacter):
    def __init__(self):
        super().__init__(
            'Papa', 'papa',
            icon_image='draft/gui/icon_images/papa_icon.png',
            preview_image='draft/gui/full_images/papa.png',
            durability=5,
            damage=5,
            utility=7,
            difficulty=5
        )

class Tim_DraftCharacter(DraftCharacter):
    def __init__(self):
        super().__init__(
            'Tim', 'tim',
            icon_image='draft/gui/icon_images/tim_icon.png',
            preview_image='draft/gui/full_images/tim.png',
            durability=1,
            damage=10,
            utility=3,
            difficulty=10
        )



character_pool_cls_list = [
    Athlea_DraftCharacter, Bizi_DraftCharacter, Bolinda_DraftCharacter, Crud_DraftCharacter, Emily_DraftCharacter, Herc_DraftCharacter, Ivan_DraftCharacter, Judy_DraftCharacter, Kane_DraftCharacter, Lu_DraftCharacter, Navi_DraftCharacter, Papa_DraftCharacter, Tim_DraftCharacter
]
   