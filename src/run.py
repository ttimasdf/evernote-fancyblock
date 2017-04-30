from evernote_fancyblock import utils, note
from evernote.api.client import EvernoteClient, NoteStore


def main(*args):
    app_token = utils.get_token()
    client = EvernoteClient(token=app_token)

    notes = note.prompt_notes(client)

    for n in notes:
        soup = note.make_soup(n)
