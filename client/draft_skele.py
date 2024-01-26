from game import Game
from drafting.client_state import DraftingState

def run():
    game = Game()
    game.state_manager.current_state = DraftingState('123', 'Greg')
    while game.is_running:
        game.game_loop()
    game.handle_close()

if __name__ == '__main__':
    run()