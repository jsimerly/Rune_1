from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from draft_team import DraftTeam


class DraftTurn:
    def __init__(self, team: DraftTeam, pick:int, is_ban:bool=False) -> None:
        self.team=team
        self.pick=pick
        self.is_ban=is_ban

class DraftPhase:
    def __init__(self, team_1: DraftTeam, team_2: DraftTeam) -> None:
        self.n_bans = 1
        self.n_picks = 3

        self.p1 = DraftTurn(team_1, 1, is_ban=True)
        self.p2 = DraftTurn(team_2, 1, is_ban=True)
        self.p3 = DraftTurn(team_1, 1) #team 1 pick 1
        self.p4 = DraftTurn(team_2, 1) #team 2 pick 1
        self.p5 = DraftTurn(team_2, 2) #team 2 pick 2
        self.p6 = DraftTurn(team_1, 2) #team 1 pick 2
        self.p7 = DraftTurn(team_1, 3) #team 1 pick 3
        self.p8 = DraftTurn(team_2, 3) #team 2 pick 3

        self.phases = [self.p1, self.p2, self.p3, self.p4, self.p5, self.p6, self.p7, self.p8]
        self.current_phase: DraftTurn = self.p1
        self.phase_index = 0
        
        self.is_complete = False

    def next_phase(self) -> bool:
        self.phase_index += 1
        print(f'phase_index: {self.phase_index} / {len(self.phases)}')
        if self.phase_index >= len(self.phases):
            self.is_complete = True
            return True
        else:
            self.current_phase = self.phases[self.phase_index]
            return False

