from enum import Enum

class DraftPhase(Enum):
    TEAM_1_BAN_1 = 1
    TEAM_2_BAN_1 = 2
    TEAM_1_PICK_1 = 3
    TEAM_2_PICK_1 = 4
    TEAM_2_PICK_2 = 5
    TEAM_1_PICK_2 = 6
    TEAM_1_PICK_3 = 7
    TEAM_2_PICK_3 = 8
    COMPLETED = 9