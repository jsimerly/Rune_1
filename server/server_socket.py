import asyncio
import websockets
import json
from state_manager import MatchMaking


match_maker = MatchMaking()
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
                        if ws_1.open:
                            asyncio.create_task(ws_1.send(game_id))
                        if ws_2.open:
                            asyncio.create_task(ws_2.send(game_id))
                    else:
                        await websocket.send('Waiting on other players...')
        except Exception as e:
            print(e)
            print("Connection closed unexpectedly.")
        finally:
            print(f'{websocket} removed.')
            await self.unregister(websocket)
    
    async def start(self):
        async with websockets.serve(self.handle_connection, self.host, self.port):
            await asyncio.Future() 

    def handle_looking_for_game(self, message, websocket):
        return match_maker.register_team(message, websocket)


if __name__ == '__main__':
    server = GameServer('localhost', 8765)
    asyncio.run(server.start())