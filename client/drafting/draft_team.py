from __future__ import annotations

from typing import TYPE_CHECKING, List, Set

class DraftCharacter:
    def __init__(self, name: str) -> None:
        self.name = name

class DraftBan:
    def __init__(self, team: DraftTeam, character: DraftCharacter) -> None:
        self.team = team
        self.character = character

class DraftPick:
    def __init__(self, team: DraftTeam, character: DraftCharacter) -> None:
        self.team = team
        self.character =  character

class DraftTeam:
    def __init__(self, team_id: str) -> None:
        self.team_id = team_id
        self.bans: Set[DraftBan] = []
        self.picks: Set[DraftPick] = []

    def ban(self, character: DraftCharacter):
        ban = DraftBan(self, character)
        self.bans.add(ban)

    def pick(self, character: DraftPick):
        pick = DraftPick(self, character)
        self.picks.add(pick)

