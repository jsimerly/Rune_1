import json

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
        
        return True, ''

    except ValueError as e:
        return False, str(e)

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