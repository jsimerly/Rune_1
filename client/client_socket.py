import asyncio
import websockets
import json
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

    async def send_data(self, message):
        async with websockets.connect(self.uri) as websocket:
            if isinstance(message, dict):
                message = json.dumps(message)
            await websocket.send(message)
            response = await websocket.recv()
            print(response)


