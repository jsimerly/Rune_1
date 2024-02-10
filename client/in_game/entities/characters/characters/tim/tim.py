import pygame as pg
from in_game.entities.characters.character_base import Character
from in_game.ecs.components.resource_component import ResourceComponent
from in_game.ecs.components.movement_component import MovementComponent
from in_game.ecs.components.health_component import HealthComponent

class Tim(Character):
    name = 'Tim'
    image_path = 'in_game/entities/characters/characters/tim/images/tim.png'
    color = (0, 148, 143) 

    def __init__(self, entity_id: str, ghost_id:str, team_id: str, is_team_1: bool) -> None:
        name = self.name

        resource_component = ResourceComponent(
            'Mana', (148, 126, 217), 
            max=5, 
            min=0,
            end_of_turn_refresh=5,
        )
        movement_component = MovementComponent(
            cost=1,
            line_color=self.color,
        )
        health_component = HealthComponent(
            max= 1000, current=1000
        )

        components = [resource_component, movement_component, health_component]
        super().__init__(entity_id, ghost_id, name, team_id, is_team_1, components=components)