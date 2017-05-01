from bs4 import BeautifulSoup
from . import utils
from evernote.api.client import NoteStore
import evernote.edam.type.ttypes as Types

def codeblock_detect(soup):
    tag_blocks = soup("pre")
    orig_blocks = soup("div", style=lambda s: isinstance(s, str) and "-en-codeblock" in s)
    fancy_blocks = soup("div", style=lambda s: isinstance(s, str) and "-en-fancyblock" in s)

    return (tag_blocks, orig_blocks, fancy_blocks)


def make_soup(note):
    text = note.content.encode()
    return BeautifulSoup(text, 'xml')


def prompt_notes(client, lazy_query=False):
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

    ret = (noteStore.getNote(notes[i-1].guid, True, False, False, False) for i in nt_selection)
    return ret if lazy_query else list(ret)


def xml_validate(soup):
    from urllib.request import urlopen
    from lxml import etree

    text = str(soup)
    if input("Validation may take a while downloading DTD file, continue? [y/N]") in 'Nn':
        return True
    with urlopen('http://xml.evernote.com/pub/enml2.dtd') as u:
        dtd = etree.DTD(u)
    t = etree.fromstring(text)
    try:
        dtd.assertValid(t)
    except etree.DocumentInvalid as e:
        print("DocumentInvalid:", e)
        return False
    else:
        return True
