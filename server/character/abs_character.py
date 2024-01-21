from abc import ABC


class AbstractCharacter_Server(ABC):
    def __init__(self) -> None:
        self.team = None
        self.speed = None
        self.strength = None

        self.leveling = None
        self.health = None
        self.resources = None
        self.map_interactions = None

        self.movement_queue = None
        self.ability_queue = None

    

    