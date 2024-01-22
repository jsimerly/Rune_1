from jsonschema import validate, ValidationError
import json

look_for_game_schema = {
    'type' : 'object',
    'properties' : {
        'type' : {'type': 'string'},
        'username' : {'type': 'string'},
    },
    'required' : ['type', 'username']
}

schema_map = {
    'lfg' : look_for_game_schema
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


    