from jsonschema import validate, ValidationError
import json
from typing import Dict

look_for_game_schema = {
    'type' : 'object',
    'properties' : {
        'type' : {'type': 'string'},
        'username' : {'type': 'string'},
    },
    'required' : ['type', 'username']
}

user_schema = {
    'type' : 'object',
    'properties' : {
        'username' : {'type': 'string'}
    },
    'required' : ['username']
}

team_schema = {
    'type' : 'object',
    'properties' : {
        'user': {'$ref': '#/definitions/user'},
        'team_id' : {'type': 'string'},
        'characters' : {'type': 'array', 'items': {'type': 'string'}},
    },
    'required' : ['user', 'team_id', 'characters'],
    'definitions' : {
        'user' : user_schema
    }
}

draft_schema = {
    'type' : 'object',
    'properties' : {
        'draft_id' : {'type': 'string'},
        'team_1' : {'$ref': '#/definitions/team'},
        'team_2' : {'$ref': '#/definitions/team'},
    },
    'required' : [],
    'definitions' : {
        'team' : team_schema
    }   
}

#drafting schema
drafting_schema = {
    'type' : 'object',
    'properties' : {
        'type': {'type': 'string'},
        'user': {'$ref': '#/definitions/user'},
        'character':{'type': 'string'},
        'pick_ban': {'type': 'string' }
        
    },
    'required': ['user', 'character', 'type', 'pick_band'],
    'definitions' : {
        'user' : user_schema
    }
}

#turn queues schem




schema_map = {
    'lfg' : look_for_game_schema
}

def validate_message(message):
    """
    Validate that the message from the client contains 'type' and 'data'.
    Additional validation can be handled in the respective objects based on 'type'.
    """
    try:
        # Check for presence of 'type' and 'data' keys
        if 'type' not in message:
            raise ValueError("Missing 'type' in message")
        if 'data' not in message:
            raise ValueError("Missing 'data' in message")
        if 'user' not in message:
            raise ValueError("missing 'user' in message")
        
        return True, ''

    except ValueError as e:
        return False, str(e)

def load_message(raw_message) -> Dict:
    try:
        message = json.loads(raw_message)
        is_valid, error = validate_message(message)
        if not is_valid:
            # handle invalid message
            print(f"Invalid message: {error}")
            return
        return message
    except json.JSONDecodeError as e:
        print(f"JSON Decode Error: {e}")


    