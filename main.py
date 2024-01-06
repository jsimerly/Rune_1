import pygame as pg
from settings import *
from map.game_map import GameMap
from game.brock_purdy import GameManager
from character.characters.crud.crud import Crud
from map.loadouts.map_1 import map_1
from game.spawning.spawning import SpawnHandler

pg.init()

screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pg.SRCALPHA)
screen.fill(BGCOLOR)
clock = pg.time.Clock()

game_map = GameMap(map=map_1, screen=screen)
#eventually attach to a team:

crud = Crud(screen=screen)
spawning_handler = SpawnHandler(crud, crud.sprite.image, (110,110), screen)

game_manager = GameManager()
game_manager.register_ui_click_event(spawning_handler.button, spawning_handler.button.on_click)
game_manager.set_game_map(game_map)
spawning_handler.draw()
game_map.draw()

is_running = True
while is_running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            is_running = False

        if event.type == pg.MOUSEBUTTONUP:
            mouse_pos = pg.mouse.get_pos()
            game_manager.handle_click(mouse_pos)

    pg.display.flip()
    clock.tick(FPS)


pg.quit()
        
        