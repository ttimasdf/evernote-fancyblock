import base64

ENC_KEY=120

def get_token():
    'TODO: Get an OAuth token from web service'
    return input("Enter your developer token: ")


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
    return bytes(c^key for c in base64.b64decode(text)).encode('ascii')
