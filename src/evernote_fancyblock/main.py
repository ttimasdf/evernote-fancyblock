from evernote_fancyblock import utils, note
from evernote.api.client import EvernoteClient


def main(*args):
    app_token, service_host = utils.get_token()
    client = EvernoteClient(token=app_token, service_host=service_host)

    notes = note.prompt_notes(client)

    for n in notes:
        print("Processing", n.title)
        soup = note.make_soup(n)
        tag_blocks, classic_blocks, fancy_blocks = note.codeblock_detect(soup)
