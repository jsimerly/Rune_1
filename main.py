import pygame as pg
from settings import *
from map.game_map import GameMap
from game.brock_purdy import GameManager
from character.characters.crud.crud import Crud
from map.loadouts.map_1 import map_1
from game.phases.spawn_handler import SpawnHandler
from game.game_phase import GamePhaseManager
from team.team import Team


pg.init()

screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pg.SRCALPHA)
screen.fill(BGCOLOR)
clock = pg.time.Clock()

game_map = GameMap(map=map_1, screen=screen)

crud = Crud(screen=screen, game_map=game_map)
crud2 = Crud(screen=screen, game_map=game_map)
crud3 = Crud(screen=screen, game_map=game_map)

team_1 = Team(team_id=1, screen=screen)
team_1.add_character(crud)
team_1.add_character(crud2)
team_1.add_character(crud3)
print(len(team_1.characters))


#need to make a game manager builder obj
game_manager = GameManager(
    game_phase_manager=team_1.game_phase_manager,
    game_map=game_map)
game_manager.register_team_1(team_1)

game_manager.set_game_map(game_map)
game_map.draw()

mouse_down_start_pos = None
drag_threshold = 60

is_running = True
while is_running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            is_running = False

        if event.type == pg.MOUSEBUTTONDOWN:
            if not mouse_down_start_pos:
                mouse_down_start_pos = pg.mouse.get_pos()
            
        if event.type == pg.MOUSEBUTTONUP:
            mouse_up_pos = pg.mouse.get_pos()
            if game_manager.is_dragging:
                game_manager.handle_drag_finish(mouse_down_start_pos, mouse_up_pos)
            else:
                game_manager.handle_click(mouse_up_pos)

            mouse_down_start_pos = None
                
        if mouse_down_start_pos and not game_manager.is_dragging:
            mouse_pos = pg.mouse.get_pos()
            dx = mouse_pos[0] - mouse_down_start_pos[0]
            dy = mouse_pos[1] - mouse_down_start_pos[1]
            distance_moved = (dx**2 + dy**2)**0.5

            if distance_moved > drag_threshold:
                game_manager.handle_drag_start(mouse_down_start_pos)

        if game_manager.is_dragging:
            game_manager.handle_drag_update(pg.mouse.get_pos())


    game_map.render.run_all()
    pg.display.flip()
    clock.tick(FPS)
    clock_time = clock.get_time()
    if clock_time > 100:
        print(clock_time)

pg.quit()
        
        