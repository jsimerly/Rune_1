from client import Client
from draft.draft_state import DraftState

def run():
    game = Client()
    draft_data = {
        'draft_id' : 123,
        'team_1': {'team_id': 123},
        'team_2': {'team_id': 123},
        'team': 1
    }
    game.state_manager.current_state = DraftState(draft_data=draft_data)
    while game.is_running:
        game.game_loop()
    game.handle_close()

if __name__ == '__main__':
    run()