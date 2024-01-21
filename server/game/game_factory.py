
class GameFactory(ServerState):
    def __init__(self) -> None:
        self.user_1 = None
        self.ws_1 = None
        self.user_2 = None
        self.ws_2 = None

    def register_team(self, user_json, websocket):
        user = user_json['user']
        if not self.user_1:
            self.user_1 = user
            self.ws_1 = websocket
        else:
            self.user_2 = user
            self.ws_2 = websocket
        
        if self.user_1 and self.user_2:
            game_id = self.start_game(self.user_1, self.user_2)
            return game_id, self.ws_1, self.ws_2
        return None, None, None

    def start_game(self, user_1, user_2):
        print(f'starting new game instance for {user_1} and {user_2}')
        self.user_1 = None
        self.user_2 = None
        return 'game_id'