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
        #draft manager to route the draftm essages
        #game manager to route the game messages

    async def add_user(self, username, websocket):
        ''' Callback for the TCP client for initial connection of a new user.'''
        user = self.user_manager.add_user(username, websocket)
        print(f'{user.username} has connected.')

    def handle_message_from_client(self, raw_message: str):
        message = load_message(raw_message)
        # abstract this away to load message, maybe
        user_data = message['user']
        if 'username' in user_data:
            username = user_data['username']
        else:
            raise ValueError('missing username in user_data')
        
        user = self.user_manager.get_user(username)
        type = message['type']
        if type == 'lfg':
            self.matchmaker.add_to_queue(user)

        #route accordingly to the proper channels.   

    def get_user(self, username):
        user = self.user_manager.get_user(username)
        if user:
            return user
        #handle this error here
        return None

    def handle_looking_for_game(self, user):
        return self.matchmaker.register_team(user)
       
if __name__ == '__main__':
    server = GameServer()
    asyncio.run(server.socket.start('localhost', 8765))