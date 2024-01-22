from typing import List, TYPE_CHECKING, Dict
from .user import User

class UsersManager:
    '''This class is used to manage all of the current users. It is essentially a quick and dirty replacement for a databse as we'll be storing users in RAM instead of hard disk'''
    def __init__(self) -> None:
        self.active_users: Dict[str, User] = {} # a map of usernames to their user object

    def connecting_user(self, username, websocket):
        if username in self.active_users:
            self.active_users[username].websocket = websocket
        else:
            self.create_user(username, websocket)
        
    def get_user(self, username):
        if username in self.active_users:
            return self.active_users[username]
        return None
    
    def create_user(self, username, websocket):
        user = User(username, websocket)
        self.active_users[username] = user

    def remove_user(self, username):
        if username in self.active_users:
            del self.active_users[username]
