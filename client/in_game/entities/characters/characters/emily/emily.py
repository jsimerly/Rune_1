import pygame as pg
from in_game.entities.characters.character_base import Character

class Emily(Character):
    def __init__(self, entity_id: str, team_id: str, is_team_1: bool) -> None:
        name = "Emily"
        sprite = pg.image.load('in_game/entities/characters/characters/emily/images/emily.png')
        super().__init__(entity_id, name, sprite, team_id, is_team_1)