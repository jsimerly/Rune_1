from typing import TYPE_CHECKING
from uuid import uuid4

if TYPE_CHECKING:
    from team.team import Team

#2 teams
class Draft:
    def __init__(self, team_1, team_2) -> None:
        self.team_1 = team_1
        self.team_2 = team_2
        #character pool
        self.bans = {"team_1":[], "team_2":[]}
        self.picks = {"team_1":[],"team_2":[]}
        self.draft_id = uuid4()
    def ban_character(self, team, character):

        #blah blah

        pass

    def pick_character(self, team, character):

        #Blah blah

        pass

    def start_draft(self):

        #blah blah

        pass

    def send_draft_results(self):

        #blah blah

        pass


