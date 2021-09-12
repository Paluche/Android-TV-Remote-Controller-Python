import json
import base64


def create_paring_request_message(client_name):
    """This function will generate JSON string for ping request message.

    :param client_name: Name of the client.

    :return: JSON string of the created message.
    """
    return json.dumps(
        {
            'protocol_version': 1,
            'payload': {
                'service_name': 'androidtvremote',
                'client_name': client_name
            },
            'type': 10,
            'status': 200
        }
    )


def create_option_message():
    """This function will generate JSON string for option message..

    :return: Message content.
    """
    return json.dumps(
        {
            'protocol_version': 1,
            'payload': {
                'output_encodings': [
                    {
                        'symbol_length': 4,
                        'type': 3
                    }
                ],
                'input_encodings': [
                    {
                        'symbol_length': 4,
                        'type': 3
                    }
                ],
                'preferred_role': 1
            },
            'type': 20,
            'status': 200
        }
    )


def create_configuration_message():
    """This function will generate JSON string for configuration message.

    :return: Message content.
    """

    return json.dumps(
        {
            'protocol_version': 1,
            'payload': {
                'encoding': {
                    'symbol_length': 4,
                    'type': 3
                },
                'client_role': 1},
            'type': 30,
            'status': 200
        }
    )


def create_secret_message(secret_hash):
    """This function will generate JSON string for secret message.

    :param secret_hash:  Client secret hash.

    :return: Message content.
    """
    return json.dumps(
        {
            'protocol_version': 1,
            'payload': {
                'secret': base64.b64encode(secret_hash).decode()
            },
            'type': 40,
            'status': 200
        }
    )


def parse_json_message(raw_data):
    """This function will parse the JSON message.

    :param raw_data:  Raw JSON message.

    :return: extracted status and type of the message
    """
    json_object = json.loads(raw_data)
    message_status = json_object['status']
    message_type = json_object['type'] if message_status == 200 else 0

    return message_status, message_type
