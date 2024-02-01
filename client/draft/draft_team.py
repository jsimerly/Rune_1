from __future__ import annotations

from typing import TYPE_CHECKING, List, Set

if TYPE_CHECKING:
    from draft_characters import DraftCharacter

class DraftBan:
    def __init__(self, team: DraftTeam, character: DraftCharacter) -> None:
        self.team = team
        self.character = character

class DraftPick:
    def __init__(self, team: DraftTeam, character: DraftCharacter) -> None:
        self.team = team
        self.character =  character

class DraftTeam:
    def __init__(self, team_id: str, username:str) -> None:
        self.team_id = team_id
        self.username = username
        self.bans: Set[DraftBan] = []
        self.picks: Set[DraftPick] = []

    def ban(self, character: DraftCharacter):
        ban = DraftBan(self, character)
        self.bans.add(ban)

    def pick(self, character: DraftPick):
        pick = DraftPick(self, character)
        self.picks.add(pick)