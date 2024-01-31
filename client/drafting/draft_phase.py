from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from draft_team import DraftTeam
class DraftTurn:
    def __init__(self, team: DraftTeam, pos, ban:bool=False) -> None:
        self.team=team
        self.pos=pos
        self.ban=ban

class DraftPhase:
    def __init__(self, team_1: DraftTeam, team_2: DraftTeam) -> None:
        self.p1 = DraftTurn(team_1, 1, ban=True)
        self.p2 = DraftTurn(team_2, 2, ban=True)
        self.p3 = DraftTurn(team_1, 3)
        self.p4 = DraftTurn(team_2, 4)
        self.p5 = DraftTurn(team_2, 5)
        self.p6 = DraftTurn(team_1, 6)
        self.p7 = DraftTurn(team_1, 7)
        self.p8 = DraftTurn(team_2, 8)

        self.phases = [self.p1, self.p2, self.p3, self.p4, self.p5, self.p6, self.p7, self.p8]
        self.phase_index = 0

        self.is_complete = False
        self.current_phase = self.p1

    def next_phase(self):
        self.phase_index += 1
        if self.phase_index > len(self.phases):
            self.is_complete = True
            return True
        self.current_phase = self.phases[self.phase_index]