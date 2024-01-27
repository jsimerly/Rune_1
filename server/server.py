from __future__ import annotations
import asyncio
import websockets
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
        draft_info = self.matchmaker.add_to_queue(user)

        if draft_info:
            user_1 = draft_info.team_1.user
            user_2 = draft_info.team_2.user
            serialized_data = json.dumps(
            {
                'type': 'game_found',
                'draft' : {
                    'draft_id': str(draft_info.draft_id),
                    'team_1': serialize_team(draft_info.team_1),
                    'team_2': serialize_team(draft_info.team_2),
                }
                
            })
            self.send_message_to_client(user_1, serialized_data)
            self.send_message_to_client(user_2, serialized_data)

    def handle_message_from_client(self, raw_message: Dict):
        #deserialize
        print(raw_message)

    def send_message_to_client(self, user: User, serialized_message: Dict):
        #serialize
        asyncio.create_task(self.socket.send_message(user, serialized_message))

    def handle_looking_for_game(self, user) -> Tuple[UUID, User, User]:
        return self.matchmaker.register_team(user)
       

if __name__ == '__main__':
    server = GameServer()
    asyncio.run(server.socket.start('localhost', 8765))