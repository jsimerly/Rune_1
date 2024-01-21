from __future__ import annotations
from building.abs_building import AbstractBuilding
from components.sprite import SpriteComponent
from components.map_interaction import MapInteractionComponent
from components.spawning import SpawningComponent
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from team.team import Team
    from map.game_tile import GameTile


class Pylon(AbstractBuilding):
    def __init__(self, tile:GameTile, team_id:int) -> None:
        super().__init__(tile=tile, team_id=team_id)
        self.team: Team = None

        self.map_interaction = MapInteractionComponent(
            is_passable = False,
            can_pierce = True,
            can_end_on = False,
            blocks_vision = False,
            hides_occupants = False,
            is_slowing = False,
            walkthrough_effects = None,
        )

        image = self.open_image('building/pylon/gui/teleporter.webp')
        self.sprite: SpriteComponent
        self.set_sprite_comp(image)
        self.sprite.move_to_tile(tile)
        self.spawning = SpawningComponent(radius=3, center_tile=tile)

    def set_team(self, team:Team):
        self.team = team



    

    

    
