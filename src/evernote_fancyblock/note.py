from bs4 import BeautifulSoup
from . import utils
from evernote.api.client import NoteStore
import evernote.edam.type.ttypes as Types
import json


STYLE_CLASSIC_BLOCK = 'box-sizing: border-box; padding: 8px; font-family: Monaco, Menlo, Consolas, "Courier New", monospace; font-size: 12px; color: rgb(51, 51, 51); border-top-left-radius: 4px; border-top-right-radius: 4px; border-bottom-right-radius: 4px; border-bottom-left-radius: 4px; background-color: rgb(251, 250, 248); border: 1px solid rgba(0, 0, 0, 0.14902); background-position: initial initial; background-repeat: initial initial;-en-codeblock:true;'
BACKUP_TAG = 'strike'

def codeblock_detect(soup):
    tag_blocks = soup("pre")
    classic_blocks = soup("div", style=lambda s: isinstance(s, str) and "-en-codeblock" in s)
    fancy_blocks = soup("div", style=lambda s: isinstance(s, str) and "-en-fancyblock" in s)

    return (tag_blocks, classic_blocks, fancy_blocks)


def make_soup(note):
    text = note.content.encode()
    return BeautifulSoup(text, 'xml')


def make_tag(string):
    return BeautifulSoup(string, 'xml').contents[0].extract()


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

    text = str(soup).encode()
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


def tag2classic(tag, soup):
    if tag.string is None:
        print("False positive:", str(tag))
        return tag

    new = soup.new_tag('div')
    new['style'] = STYLE_CLASSIC_BLOCK
    for s in tag.string.split('\n'):
        p = soup.new_tag('div')
        p.string = s
        if p.string.strip() == '':
            p.append(soup.new_tag('br'))
        new.append(p)

    backup_replace_tag(tag, new, soup)
    return new


def backup_replace_tag(orig, new, soup):
    bk_sec = orig.find(BACKUP_TAG)
    if bk_sec is None:
        bk_sec = soup.new_tag(BACKUP_TAG)
    else:
        bk_sec.extract()

    try:
        payload = json.loads(bk_sec['title'])
    except (KeyError, json.JSONDecodeError) as e:
        print("Backup not found", e)
        payload = {}

    if payload.get('orig') is None:
        payload['orig'] = str(orig)
    payload['last'] = str(orig)

    bk_sec['title'] = json.dumps(payload)
    new.insert(0, bk_sec)
    orig.replace_with(new)

    return new


def restore_tag(tag, soup):
    bk_sec = tag.find(BACKUP_TAG)
    try:
        payload = json.loads(bk_sec['title'])
    except (TypeError, KeyError, json.JSONDecodeError) as e:
        print("Backup not found", e)
        return
    new = make_tag(payload['orig'])
    tag.replace_with(new)
    return new

