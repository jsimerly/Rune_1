from typing import TYPE_CHECKING
from uuid import uuid4
from enum import Enum

if TYPE_CHECKING:
    from team.team import Team


class DraftPhase(Enum):
    BAN1_TEAM1 = "Ban 1 - Team 1"
    BAN2_TEAM2 = "Ban 2 - Team 2"
    PICK1_TEAM1 = "Pick 1 - Team 1"
    PICK2_3_TEAM2 = "Pick 2/3 - Team 2"
    PICK4_5_TEAM1 = "Pick 4/5 - Team 1"
    PICK6_TEAM2 = "Pick 6 - Team 2"


class Draft:
    def __init__(self, team_1, team_2) -> None:
        self.team_1 = team_1
        self.team_2 = team_2
        self.bans = {"team_1":[], "team_2":[]}
        self.picks = {"team_1":[],"team_2":[]}
        self.draft_id = uuid4()
        self.character_pool = {
            "Crud":{"role": "Tank"},
            "Herc":{"role": "Tank"},
            "Kane":{"role": "Tank"},
            "Emilie":{"role": "Healer"},
            "Athlea":{"role": "Healer"},
            "Bizi":{"role": "Healer"},
            "Judy":{"role": "MDPS"},
            "Papa":{"role": "MDPS"},
            "Tim":{"role": "RDPS"},
            "Bolinda":{"role": "RDPS"},
            "Lu":{"role": "Jungle"},
            "Navi":{"role": "Jungle"},
            "Ivan":{"role": "Jungle"}
        }

    def next_phase(self):
        # Switch between the six phases
        current_phase_index = DraftPhase.__members__.values().index(self.current_phase)
        next_phase_index = (current_phase_index + 1) % len(DraftPhase)
        self.current_phase = list(DraftPhase)[next_phase_index]

    def ban_character(self, team, character):

        #To Do
        pass

    def pick_character(self, team, character):

        #To Do

        pass

    def start_draft(self):

        #To Do

        pass

    def send_draft_results(self):

        #To Do

        pass


