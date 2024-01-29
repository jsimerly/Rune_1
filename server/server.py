from __future__ import annotations
import asyncio
import json
from match_maker import MatchMaking
from user.users_manager import UsersManager
from api import load_message
from uuid import UUID
import traceback
from typing import TYPE_CHECKING, Tuple, Optional, Dict
from server_socket import TCPServer
import asyncio
from serializer import serialize_team, serialize_user

if TYPE_CHECKING:
    from user.user import User

class GameServer:
    def __init__(self) -> None:
        self.socket = TCPServer(self.add_user, self.handle_message_from_client)
        
        self.user_manager = UsersManager()
        self.matchmaker = MatchMaking()

    async def add_user(self, username, websocket):
        user = self.user_manager.add_user(username, websocket)
        self.matchmaker.add_to_queue(user)


    def handle_message_from_client(self, raw_message: Dict):
        print(raw_message)
        print('------------ from client listening ------------------')
        #route accordingly to the proper channels.   


    def handle_looking_for_game(self, user) -> Tuple[UUID, User, User]:
        return self.matchmaker.register_team(user)
       

if __name__ == '__main__':
    server = GameServer()
    asyncio.run(server.socket.start('localhost', 8765))