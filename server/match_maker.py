from __future__ import annotations
from typing import Protocol, TYPE_CHECKING, Tuple, Optional
import asyncio
from drafting.draft_factory import DraftFactory
from server_socket import TCPServer
import json

if TYPE_CHECKING:
    from user.user import User
    from drafting.draft import Draft

class MatchMaking:
    def __init__(self) -> None:
        self.user_1 = None
        self.user_2 = None
        self.draft_factory = DraftFactory()
        self.socket = TCPServer()

    def add_to_queue(self, user: User) -> Optional[Draft]:
        if not self.user_1:
            self.user_1 = user
        else:
            self.user_2 = user
        
        if self.user_1 and self.user_2:
            draft_obj = self.start_draft(self.user_1, self.user_2)
            self.user_1 = None
            self.user_2 = None
            
            self.notify_players_of_draft(draft_obj)
            return draft_obj

        return None
    
    def start_draft(self, user_1: User, user_2: User) -> Draft:
        print(f'Starting a draft between {user_1.username} vs {user_2.username}')
        # return serializered game information here including the uuid and opponent.
        draft_obj = self.draft_factory.create(user_1, user_2)
        return draft_obj
    

    def notify_players_of_draft(self, draft_obj: Draft):
        #serializer draft here
        serialized_draft_obj = draft_obj.serialize()
        package_1 = json.dumps({
            'type': 'game_found',
            'data': {
                **serialized_draft_obj,
                'team': 1,
            }
        }) 
        package_2 = json.dumps({
            'type': 'game_found',
            'data': {
                **serialized_draft_obj,
                'team': 2,
            }
        }) 

        user_1 = draft_obj.team_1.user
        user_2 = draft_obj.team_2.user
        self.socket.send_message(user_1, package_1)
        self.socket.send_message(user_2, package_2)


