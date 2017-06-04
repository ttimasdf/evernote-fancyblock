from . import utils, note, options
from evernote.api.client import EvernoteClient
from time import time


def main():
    args = options.get_args()
    app_token, service_host = utils.get_token()
    client = EvernoteClient(token=app_token, service_host=service_host)
    store = client.get_note_store()

    notes = note.prompt_notes(client)

    for n in notes:
        print("Processing [[", n.title, "]]")
        soup = note.make_soup(n)
        tag_blocks, classic_blocks, fancy_blocks = note.codeblock_detect(soup)

        if args.restore:
            for blk in tag_blocks + classic_blocks + fancy_blocks:
                note.restore_tag(blk, soup)
            print(len(tag_blocks) + len(classic_blocks) + len(fancy_blocks),
                  "blocks restored")
        if args.tag:
            if classic_blocks:
                print("NotImplemented: classic2tag")
            if fancy_blocks:
                print("NotImplemented: fancy2tag")
        elif args.classic:
            if tag_blocks:
                for c in tag_blocks:
                    note.tag2classic(c, soup)
                print(len(tag_blocks), "tag blocks processed!")
            if fancy_blocks:
                print("NotImplemented: fancy2classic")
        elif args.fancy:
            if tag_blocks:
                print("NotImplemented: tag2fancy")
            if classic_blocks:
                print("NotImplemented: classic2fancy")
        else:
            print("SKIPPED transformation phase")

        if args.lock:
            n.attributes.contentClass = "com.github.evernote-fancyblock"
            print("Note locked")
        elif args.unlock:
            n.attributes.contentClass = None
            print("Note unlocked")

        n.content = str(soup)
        n.updated = int(time() * 1000)
        store.createNote(n)
