from __future__ import annotations

from in_game.ecs.entity import Entity
from .system_base import System
from in_game.ecs.components.team_component import TeamComponent


from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from entity import Entity

class TeamSystem(System):
    required_components = [TeamComponent]

    def on_same_team(self, entity_1: Entity, entity_2: Entity):
        entity_1_team_comp: TeamComponent = entity_1.get_component(TeamComponent)
        entity_2_team_comp: TeamComponent = entity_2.get_component(TeamComponent)
        return entity_1_team_comp.team_id == entity_2_team_comp.team_id
    


