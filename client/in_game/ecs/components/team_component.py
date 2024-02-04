from in_game.ecs.components.component_base import Component
from dataclasses import dataclass

@dataclass
class TeamComponent(Component):
    team_id: str
    is_team_1: bool