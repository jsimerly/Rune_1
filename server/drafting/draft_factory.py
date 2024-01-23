from drafting.draft import Draft

class DraftFactory:
    def create(self, team_1, team_2):
        
        return Draft(team_1 = team_1, team_2 = team_2)
    
    def get_map(self):
        return "map_1"
