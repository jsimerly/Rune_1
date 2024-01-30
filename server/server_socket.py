from __future__ import annotations
import asyncio
import websockets
import json
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
    
    def __init__(self, add_user_callback: Callable=None, handle_message: Callable=None):
        if self.__initialized:
            return        
        
        if add_user_callback is None or handle_message is None:
            raise ValueError("Initial instantiation of TCPServer requires 'add_user_callback' and 'handle_message' parameters")

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

    def send_message(self, user: User, type: str, serialized_message:str):
        asyncio.create_task(self._send_message(user, type, serialized_message))

    async def _send_message(self, user: User, type:str, package: str):
        #need to handle types here as just like on the client side 
        message = json.dumps({
            'type': type,
            'data': package,
        })
        if user.websocket in self.clients:
            await user.websocket.send(message)

    async def start(self, host, port):
        async with websockets.serve(self.handle_connections, host, port):
            print(f"Server started on {host}:{port}")
            await asyncio.Future()  # Run forever

    
