from .draft_team import DraftCharacter

class Athlea_Draft(DraftCharacter):
    def __init__(self) -> None:
        super().__init__('Athlea')

class Bizi_Draft(DraftCharacter):
    def __init__(self):
        super().__init__('Bizi')

class Bolinda_Draft(DraftCharacter):
    def __init__(self):
        super().__init__('Bolinda')

class Crud_Draft(DraftCharacter):
    def __init__(self):
        super().__init__('Crud')

class Emily_Draft(DraftCharacter):
    def __init__(self):
        super().__init__('Emily')

class Herc_Draft(DraftCharacter):
    def __init__(self):
        super().__init__('Herc')

class Ivan_Draft(DraftCharacter):
    def __init__(self):
        super().__init__('Ivan')

class Judy_Draft(DraftCharacter):
    def __init__(self):
        super().__init__('Judy')

class Kane_Draft(DraftCharacter):
    def __init__(self):
        super().__init__('Kane')

class Lu_Draft(DraftCharacter):
    def __init__(self):
        super().__init__('Lu')

class Navi_Draft(DraftCharacter):
    def __init__(self):
        super().__init__('Navi')

class Papa_Draft(DraftCharacter):
    def __init__(self):
        super().__init__('Papa')

class Tim_Draft(DraftCharacter):
    def __init__(self):
        super().__init__('Tim')


draft_pool_map = {
    'athlea': Athlea_Draft, 
    'bizi': Bizi_Draft, 
    'bolinda': Bolinda_Draft, 
    'crud': Crud_Draft, 
    'emily': Emily_Draft,
    'herc': Herc_Draft, 
    'ivan': Ivan_Draft, 
    'judy': Judy_Draft, 
    'kane': Kane_Draft, 
    'lu': Lu_Draft, 
    'navi': Navi_Draft, 
    'papa': Papa_Draft,
    'tim': Tim_Draft
}

