from user.user import User
from uuid import uuid4

class Team:
    def __init__(self, user: User) -> None:
        self.user: User = user
        self.team_id = uuid4()
        self.characters = []
        self.buildings = []

    