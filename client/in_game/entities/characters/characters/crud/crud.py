import pygame as pg
from in_game.entities.characters.character_base import Character
from in_game.ecs.components.resource_component import ResourceComponent
from in_game.ecs.components.movement_component import MovementComponent
from in_game.ecs.components.health_component import HealthComponent


class Crud(Character):
    name = 'Crud'
    image_path = 'in_game/entities/characters/characters/crud/images/crud.png'
    color = (145, 23, 1)

    def __init__(self, entity_id: str, team_id: str, is_team_1: bool) -> None:
        name = self.name
        sprite = pg.image.load(self.image_path)
        ghost_sprite = pg.image.load(self.image_path)
        ghost_sprite = pg.transform.scale(ghost_sprite, self.ghost_size)
        ghost_sprite.set_alpha(self.ghost_alpha)

        resource_component = ResourceComponent(
            'Rage', (191, 25, 10), 
            max=10, 
            min=0,
            end_of_turn_refresh=5,
            bonus_type='rage'
        )
        movement_component = MovementComponent(
            movement_cost=1,
            movement_line_color=self.color,
            ghost_image=ghost_sprite
        )
        health_component = HealthComponent(
            max= 1000, current=1000
        )

        components = [
            resource_component, 
            movement_component, 
            health_component,
        ]
        super().__init__(entity_id, name, sprite, team_id, is_team_1, components=components)


