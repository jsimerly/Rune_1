import asyncio
import websockets
import json
from uuid import uuid4
from typing import Callable


class TCPClient:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(TCPClient, cls).__new__(cls)
            cls._instance.__initialized = False
        return cls._instance
    
    def __init__(self):
        if self.__initialized:
            return
        self.__initialized = True
        self.uri = 'ws://localhost:8765'
        self.loop = asyncio.get_event_loop()
        self.websocket = None
    
    async def connect(self):
        self.websocket = await websockets.connect(self.uri)
        await self.start_listening()

    async def close_connection(self):
        await self.websocket.close()

    def create_task(self, task: Callable):
        self.loop.create_task(task)

    def run_one(self):
        self.loop.call_soon(self.loop.stop)
        self.loop.run_forever()

    async def send_data(self, message, type):
        if type not in ['looking_for', 'draft', 'player_queues', 'end_game']:
            raise ValueError("Type must be one of the following: looking_for', 'draft', 'player_queues', 'end_game'")
        
        if not isinstance(message, dict):
            raise ValueError('messages must be a dictionary or json format to be sent using send_data.')
    
        if not self.websocket:
            await self.connect()
            


        package = {
            'type': type,
            'message': message
        }
        package = json.dumps(package)
        await self.websocket.send(package)
        # response = await self.websocket.recv()
        # return response
    
    async def listen_for_messages(self):
        while True:
            message = await self.websocket.recv()
            print(message)
    
    async def start_listening(self):
        asyncio.create_task(self.listen_for_messages())



            


