import asyncio
import websockets
import json
from state_manager import GameFactory

game_factory = GameFactory()

class GameServer:
    def __init__(self, host, port) -> None:
        self.host = host
        self.port= port
        self.connections = set()

    async def register(self, websocket):
        self.connections.add(websocket)

    async def unregister(self, websocket):
        self.connections.remove(websocket)

    async def handle_connection(self, websocket, path):
        await self.register(websocket)
        try:
            async for message in websocket:
                data = json.loads(message)
                if data['type'] == 'looking_for':
                    game_id, ws_1, ws_2 = self.handle_looking_for_game(data['message'], websocket)

                    if game_id != None:
                        asyncio.create_task(ws_1.send(game_id))
                        asyncio.create_task(ws_2.send(game_id))
                    else:
                        await websocket.send('Waiting on other players...')
        finally:
            print("REMOVED CONNECTION")
            self.connections.remove(websocket)
    
    async def start(self):
        async with websockets.serve(self.handle_connection, self.host, self.port):
            await asyncio.Future() 

    def handle_looking_for_game(self, message, websocket):
        return game_factory.register_team(message, websocket)


if __name__ == '__main__':
    server = GameServer('localhost', 8765)
    asyncio.run(server.start())