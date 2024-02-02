
from client import Client
from in_game.client_state import InGameState



def run():
    game = Client()
    game_data = {}
    game_state = InGameState(game_data)

    game.state_manager.current_state = game_state
    while game.is_running:
        game.game_loop()
    game.handle_close()

if __name__ == '__main__':
    run()
