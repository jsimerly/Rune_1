import pygame as pg
from client.settings import *
from client.in_game.game_manager import GameManager
from client.in_game.action_state import Click, DragStart, DragEnd
# from character.characters.crud.crud import Crud
# from character.characters.emilie.emilie import Emilie
from map.loadouts.map_1 import map_1
# from team.team import Team
from server.turn_event_manager import TurnManager

pg.init()

screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pg.SRCALPHA)
screen.fill(BGCOLOR)
clock = pg.time.Clock()

team_1 = Team(team_id=1)
game_manager = GameManager(map_1, screen, team_1)
crud = Crud()
emilie = Emilie()
game_manager.add_character(crud)
game_manager.add_character(emilie)

turn_manager = TurnManager(game_manager)
game_manager.end_turn_callback = turn_manager.team_1_end_turn

mouse_down_start_pos = None
is_dragging = False
drag_threshold = 50

def drag_threshold_reached(mouse_pos):
    dx = mouse_pos[0] - mouse_down_start_pos[0]
    dy = mouse_pos[1] - mouse_down_start_pos[1]
    distance = (dx**2 + dy**2)**0.5
    return distance > drag_threshold

is_running = True
while is_running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            is_running = False

        mouse_pos = pg.mouse.get_pos()
        if event.type == pg.MOUSEBUTTONDOWN:
            if not mouse_down_start_pos:
                mouse_down_start_pos = mouse_pos
            
        if event.type == pg.MOUSEBUTTONUP:
            if is_dragging:
                game_manager.input(DragEnd(mouse_pos))
            else:
                game_manager.input(Click(mouse_pos))

            mouse_down_start_pos = None
            is_dragging = False

        if mouse_down_start_pos and not is_dragging:
            if drag_threshold_reached(mouse_pos):
                game_manager.input(DragStart(mouse_pos))
                is_dragging = True

        if is_dragging:
            game_manager.update(mouse_pos)
            
        game_manager.surfaces.draw()

    pg.display.flip()
    clock.tick(FPS)
    clock_time = clock.get_time()
    if clock_time > 200:
        print(clock_time)

pg.quit()
        
        