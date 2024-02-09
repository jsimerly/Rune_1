import pygame as pg
from in_game.entities.characters.character_base import Character

class Tim(Character):
    def __init__(self, entity_id: str, team_id: str, is_team_1: bool) -> None:
        name = "Tim"
        sprite = pg.image.load('in_game/entities/characters/characters/tim/images/tim.png')
        super().__init__(entity_id, name, sprite, team_id, is_team_1)