from pathlib import Path
from configparser import ConfigParser
from evernote_fancyblock import utils, note
from evernote.api.client import EvernoteClient, NoteStore


def main(*args):
    config_file = Path('config.ini')
    config_file.touch(mode=0o644)

    parser = ConfigParser()

    with config_file.open() as f:
        parser.read_file(f)

    if parser.has_section('secret'):
        app_token = utils.decrypt(parser.get('secret', 'token'))
    else:
        app_token = utils.get_token()
        parser.add_section('secret')
        parser.set('secret', 'token', utils.encrypt(app_token))

    client = EvernoteClient(token=app_token)

    notes = note.prompt_notes(client)

