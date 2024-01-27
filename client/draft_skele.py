from client import Client
from drafting.client_state import DraftingState

def run():
    game = Client()
    draft_data = {
        'draft_id' : 123,
        'team_1': 455,
        'team_2': 789,
    }
    game.state_manager.current_state = DraftingState(draft_data=draft_data)
    while game.is_running:
        game.game_loop()
    game.handle_close()

if __name__ == '__main__':
    run()