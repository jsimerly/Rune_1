import asyncio
import websockets
import json
from uuid import uuid4
from typing import Callable, Dict
from api.api_schema import load_message


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
        self.message_callback = None
    
    async def connect(self):
        self.websocket = await websockets.connect(self.uri)
        await self.start_listening()

    async def close_connection(self):
        if self.websocket:
            await self.websocket.close()

    def create_task(self, task: Callable):
        self.loop.create_task(task)

    def run_one(self):
        self.loop.call_soon(self.loop.stop)
        self.loop.run_forever()

    async def send_data(self, username: str, type: str,  data: Dict):
        if type not in ['lfg', 'draft', 'player_queues', 'end_game']:
            raise ValueError("Type must be one of the following: looking_for', 'draft', 'player_queues', 'end_game'")
        
        if not isinstance(data, dict):
            raise ValueError('messages must be a dictionary or json format to be sent using send_data.')
    
        if not self.websocket:
            await self.connect()
        

        package = {
            'type': type,
            'username': username,
            'data': data,
        }
        package = json.dumps(package)
        await self.websocket.send(package)
        # response = await self.websocket.recv()
        # return response
    
    async def listen_for_messages(self):
        while True:
            message = await self.websocket.recv()
            message = load_message(message)
            self.message_callback(message)

    ''''NEED TO ROUTE THIS TO WHATEVER THE CODE IS. THIS IS WHERE ALL OUR CONNECTIONS WILL COME FROm.'''
    
    async def start_listening(self):
        asyncio.create_task(self.listen_for_messages())



            


