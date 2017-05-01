from evernote_fancyblock import utils, note
from evernote.api.client import EvernoteClient


def main(*args):
    app_token = utils.get_token()
    client = EvernoteClient(token=app_token)

    notes = note.prompt_notes(client)

    for n in notes:
        soup = note.make_soup(n)
        tag_blocks, orig_blocks, fancy_blocks = note.codeblock_detect(soup)
