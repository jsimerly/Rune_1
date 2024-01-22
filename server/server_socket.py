from __future__ import annotations
import asyncio
import websockets
import json
from match_maker import MatchMaking
from user.users_manager import UsersManager
from api import load_message
from uuid import UUID
import traceback
from typing import TYPE_CHECKING, Tuple, Optional

if TYPE_CHECKING:
    from user.user import User

match_maker = MatchMaking()
class GameServer:
    def __init__(self, host, port) -> None:
        self.host = host
        self.port= port
        self.user_manager = UsersManager()
        print(f'Server has started running on {host}:{port}.')

    async def register(self, username, websocket):
        self.user_manager.create_user(username, websocket)

    async def unregister(self, username):
        self.user_manager.remove_user(username)

    async def handle_connection(self, websocket, path):
        print('New Connection Established')
        try:
            first_message = await websocket.recv()
            username = json.loads(first_message).get('username')
            await self.register(username, websocket)
            print('User Regsitered: ', username)

            user = self.user_manager.get_user(username)
            if user:
                game_info = self.handle_looking_for_game(user) 
                if game_info is not None:
                    game_id = game_info['game_id']
                    user_1 = game_info['user_1']
                    user_2 = game_info['user_2']
                    print(game_id)
                    print(user_1)
                    print(user_2)
                    await self.notify_players_of_game(game_id, user_1, user_2)

            #sync recieving any new messages from the websocket
            async for raw_message in websocket:
                #this does validation to make sure it's proper schema\
                data = load_message(raw_message) 
                user = self.user_manager.get_user(data['username'])
                if not user:
                    raise ValueError('No user with that username exists.')

        except Exception as e:
            print("Connection closed unexpectedly.")
            traceback.print_exc()
        finally:
            print(f'{websocket} removed.')
            await self.unregister(websocket)
    
    async def start(self):
        async with websockets.serve(self.handle_connection, self.host, self.port):
            await asyncio.Future() 

    def handle_looking_for_game(self, user) -> Tuple[UUID, User, User]:
        return match_maker.register_team(user)
    
    async def notify_players_of_game(self, game_id, user_1: User, user_2: User):
            if user_1.websocket.open:
                asyncio.create_task(user_1.websocket.send(str(game_id)))
            if user_2.websocket.open:
                asyncio.create_task(user_2.websocket.send(str(game_id)))


if __name__ == '__main__':
    server = GameServer('localhost', 8765)
    asyncio.run(server.start())