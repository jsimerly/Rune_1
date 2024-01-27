from __future__ import annotations
import asyncio
import websockets
import json
from match_maker import MatchMaking
from user.users_manager import UsersManager
from api import load_message
from uuid import UUID
import traceback
from typing import TYPE_CHECKING, Tuple, Optional, Callable, Dict

if TYPE_CHECKING:
    from user.user import User

class TCPServer:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(TCPServer, cls).__new__(cls)
            cls._instance.__initialized = False
        return cls._instance
    
    def __init__(self, add_user_callback: Callable, handle_message: Callable):
        if self.__initialized:
            return        
        self.__initialized = True
        self.add_user_callback = add_user_callback
        self.handle_message_callback = handle_message
        self.clients = set()


    async def handle_connections(self, websocket, path):
        self.clients.add(websocket)
        await self.add_user(websocket)
        try:
            await self.listen_for_messages(websocket)
        finally:
            self.clients.remove(websocket)

    async def add_user(self, websocket):
        try:
            first_message = await websocket.recv()
            username = json.loads(first_message).get('username')

            if username:
                await self.add_user_callback(username, websocket)
            else:
                print("Username not provided in the first message")
        except json.JSONDecodeError:
            print("Received non-JSON message as first message")
        except KeyError:
            print("Received JSON message without 'username' key")

    async def listen_for_messages(self, websocket):
        async for raw_messages in websocket:
            self.handle_message_callback(raw_messages)

    async def send_message(self, user: User, package: Dict):
        if user.websocket in self.clients:
            await user.websocket.send(package)

    async def start(self, host, port):
        async with websockets.serve(self.handle_connections, host, port):
            print(f"Server started on {host}:{port}")
            await asyncio.Future()  # Run forever

    
