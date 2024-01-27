from drafting.draft import Draft
from team.team import Team
from user.user import User

class DraftFactory:
    def create(self, user_1: User, user_2: User):
        team_1 = Team(user_1)
        team_2 = Team(user_2)
        return Draft(team_1 = team_1, team_2 = team_2)
    
    def get_map(self):
        return "map_1"
