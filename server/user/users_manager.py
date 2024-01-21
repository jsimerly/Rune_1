from typing import List, TYPE_CHECKING, Dict
from user import User

class UsersManager:
    '''This class is used to manage all of the current users. It is essentially a quick and dirty replacement for a databse as we'll be storing users in RAM instead of hard disk'''
    def __init__(self) -> None:
        self.active_users: Dict[str, User] = [] # a map of usernames to their user object
        
    def create_user(self, username, websocket):
        user = User(username, websocket)
        self.active_users[username] = user

    def remove_user(self, username):
        if username in self.active_users:
            del self.active_users[username]