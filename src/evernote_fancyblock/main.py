from . import utils, note
from evernote.api.client import EvernoteClient
from time import time


def main():
    app_token, service_host = utils.get_token()
    client = EvernoteClient(token=app_token, service_host=service_host)
    store = client.get_note_store()

    notes = note.prompt_notes(client)

    for n in notes:
        print("Processing [[", n.title, "]]")
        soup = note.make_soup(n)
        tag_blocks, classic_blocks, fancy_blocks = note.codeblock_detect(soup)

        if classic_blocks:
            if input("Found classic blocks! restore?") != "y":
                continue
            for c in classic_blocks:
                note.restore_tag(c, soup)
            print(len(classic_blocks), "blocks processed!")
        else:
            for c in tag_blocks:
                note.tag2classic(c, soup)
            print(len(tag_blocks), "blocks processed!")

        n.content = str(soup)
        # n.updated = int(time()*1000)
        store.updateNote(n)
