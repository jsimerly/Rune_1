from .game_events import OnClickEventManager
from game.clickable_obj import AbstractClickableObject, ContinueClickAction
from typing import List
from map.game_map import GameMap, GameTile
from .game_phase import GamePhase, GamePhaseManager
from team.team import Team


class GameManager:
    '''
        This will eventually turn into the client side handler so we're only building out a single team's capabilities. It will have to connect to a server to resolve async turns.
    '''
    def __init__(self, game_phase_manager: GamePhaseManager, game_map:GameMap) -> None:
        self.ui_click_events = OnClickEventManager()
        self.ui_objects: List[AbstractClickableObject] = []
        self.next_click_function = None
        self.game_phase_manager: GamePhaseManager = game_phase_manager
        
        self.team_1: Team = None

        self.game_map: GameMap = game_map
        for tile in self.game_map.tiles.values():
            tile.set_game_phase(self.game_phase_manager)

        self.is_dragging: bool = False

    def set_game_map(self, game_map: GameMap):
        self.game_map = game_map

    def register_team_1(self, team: Team):
        self.team_1 = team
        for spawn_handler in team.spawn_handlers.values():
           spawn_button = spawn_handler.button
           self.register_ui_click_event(spawn_button)

        self.register_ui_click_event(team.game_phase_manager.next_phase_button)
        self.register_ui_click_event(team.game_phase_manager.prev_phase_button)


    def register_ui_click_event(self, obj: AbstractClickableObject):
        self.ui_objects.append(obj)
        self.ui_click_events.register_event(obj=obj, fn=obj.on_click)

    def unregister_ui_click_event(self, obj):
        self.ui_objects.remove(obj)
        self.ui_click_events.unregister(obj)

    def get_tile_from_pixel(self, pixel_coord) -> GameTile:
        hex_coord = self.game_map.layout.pixel_to_hex_coord(pixel_coord)
        q, r, s = hex_coord
        try:
            return self.game_map.tiles[(q,r)]
        except KeyError:
            return None

    def find_clicked_obj(self, mouse_pos) -> AbstractClickableObject:
        for obj in self.ui_objects:
            if obj.rect.collidepoint(mouse_pos):
                return obj
            
        return self.get_tile_from_pixel(mouse_pos)

    def handle_click(self, mouse_pos):
        clicked_obj = self.find_clicked_obj(mouse_pos)

        if clicked_obj:
            ''' If we are already in the middle of a clicking chain for an in game action we'll handle that. If not this is the first click and we can handle that now.'''
            if self.next_click_function:
                next_click_function = self.next_click_function(clicked_obj)

                if next_click_function == ContinueClickAction: #check if we should stay on the same action or move to the next.
                    return
                
                self.next_click_function = next_click_function

            else:
                self.next_click_function = clicked_obj.on_click()

    def handle_drag_start(self, mouse_down_pos):
        self.is_dragging = True
        print('start dragging')

    def handle_drag_update(self, mouse_pos):
        print(mouse_pos)

    def handle_drag_finish(self, mouse_down_pos, mouse_up_pos):
        self.is_dragging = False
        print('finish dragging')


    
