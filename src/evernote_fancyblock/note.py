from bs4 import BeautifulSoup
from . import utils
from evernote.api.client import EvernoteClient, NoteStore


def codeblock_detect(soup):
    orig_blocks = soup("pre")
    fancy_blocks = soup("div", style=lambda s: isinstance(s, str) and "-en-codeblock" in s)
    modified_blocks = soup("div", style=lambda s: isinstance(s, str) and "-en-fancyblock" in s)

    return (orig_blocks, fancy_blocks, modified_blocks)


def make_soup(note):
    text = note.content
    return BeautifulSoup(text, 'xml')


def prompt_notes(client):
    print("Fetching notebooks...\n")
    noteStore = client.get_note_store()
    notebooks = noteStore.listNotebooks()
    for i in range(len(notebooks)):
        print("[{num}] {name}".format(num=i+1, name=notebooks[i].name))

    nb_selection = int(input("Select notebooks[1-{}]:".format(len(notebooks))))
    assert nb_selection in range(1, len(notebooks)+1), "Notebook selection out of range"
    nb = notebooks[nb_selection-1]

    note_filter = NoteStore.NoteFilter()
    note_filter.notebookGuid = nb.guid
    spec = NoteStore.NotesMetadataResultSpec()
    spec.includeTitle = True
    note_metas = noteStore.findNotesMetadata(note_filter, 0, 100, spec)
    notes = note_metas.notes
    for i in range(len(notes)):
        print("[{num}] {name}".format(num=i+1, name=notes[i].title))

    nt_selection = utils.set_from_range(input("Select notes[1-{}]:".format(len(notes))))
    assert nt_selection.issubset(range(1, len(notes)+1)), "Note selection out of range"

    return (noteStore.getNote(notes[i-1].guid, True, False, False, False) for i in nt_selection)

