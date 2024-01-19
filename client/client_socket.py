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
        
        
        async with websockets.connect(self.uri) as websocket:
            package = {
                'type': type,
                'message': message
            }
            package = json.dumps(package)
            await websocket.send(package)
            response = await websocket.recv()
            print(response)


            


