from pathlib import Path
from configparser import ConfigParser
import base64

ENC_KEY = 120
CONFIG_FILE = 'config.ini'

def get_token():
    config_file = Path(CONFIG_FILE)
    config_file.touch(mode=0o644)

    parser = ConfigParser()

    with config_file.open() as f:
        parser.read_file(f)

    if parser.has_section('secret'):
        app_token = decrypt(parser.get('secret', 'token'))
    else:
        app_token = input("Enter your developer token: ")
        parser.add_section('secret')
        parser.set('secret', 'token', encrypt(app_token))

    return app_token


def set_from_range(input_numbers):
    selected_numbers = []
    for part in input_numbers.split(','):
            x = part.split('-')
            if len(x) == 1:
                selected_numbers.append(int(x[0]))
            elif len(x) == 2:
                selected_numbers.extend(range(int(x[0]), int(x[1])+1))
            else:
                print("Error, your input seems illegal." + str(len(x)))
                return None
    return set(selected_numbers)


def encrypt(text, key=ENC_KEY):
    if isinstance(text, str):
        text = text.encode()
    assert isinstance(text, bytes)
    return base64.b64encode(bytes(c^key for c in text)).decode('ascii')


def decrypt(text, key=ENC_KEY):
    if isinstance(text, str):
        text = text.encode()
    assert isinstance(text, bytes)
    return bytes(c^key for c in base64.b64decode(text)).decode('ascii')
