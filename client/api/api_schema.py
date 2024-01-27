from jsonschema import validate, ValidationError
import json

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
        'team_1' : {'type': 'string'},
        'team_2': {'type': 'string'},
        'team_1' : {'$ref': '#/definitions/team'},
        'team_2' : {'$ref': '#/definitions/team'},
    },
    'required' : [],
    'definitions' : {
        'team' : team_schema
    }   
}

game_schema = {
    'type' : 'object',
    'properties' : {
        'game_id' : {'type': 'string'},
        'team_1' : {'$ref': '#/definitions/team'},
        'team_2' : {'$ref': '#/definitions/team'},
        'round' : {'type': 'integer'},
    },
    'required' : [],
    'definitions' : {
        'team' : team_schema
    }
}

game_found_schema = {
    'type' : 'object',
    'properties' : {
        'type' : {'type' : 'string'},
        'draft' : {'$ref': '#/definitions/draft'}
    },
    'required': ['type', 'draft'],
    'definitions' : {
        'draft': draft_schema,
        'user': user_schema,
        'team': team_schema,
    }
}

schema_map = {
    'game_found' : game_found_schema
}

def validate_message(message):
    '''
        We're using this function to validate that the message that was sent from the client is in a proper formate based on the 'type' that was sent. We'll need to build a simliar schema on the client to route moves.
    '''
    try:
        # Extract message type
        message_type = message.get('type')
        if message_type not in schema_map:
            raise ValidationError(f"Invalid message type: {message_type}")

        # Get the corresponding schema and validate
        schema = schema_map[message_type]
        validate(instance=message, schema=schema)
    except ValidationError as e:
        return False, str(e)
    except KeyError as e:
        return False, f"Key error: {str(e)}"
    return True, ""

def load_message(raw_message):
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