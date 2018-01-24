# evernote-fancyblock
Prettify codeblocks in Evernote notes, especially pages from web clipper.

*EDIT: This script does NOT work anymore for evernote [disabled developer token for security concerns](https://discussion.evernote.com/topic/108911-developer-token-are-not-supported-anymore/).*

# Usage
## Get Developer Token

Simply run `./run.py`. For the first time, it will prompt you of your developer token.

To get your token from different services:
- [www.evernote.com](https://www.evernote.com/api/DeveloperToken.action)
- [app.yinxiang.com](https://app.yinxiang.com/api/DeveloperToken.action)
- [sandbox.evernote.com](https://sandbox.evernote.com/api/DeveloperToken.action)

Simply enter the token when it asked and it'll be encrypted and stored in `config.ini` locally. If you want to use this program in production (Use a real account other than a faked one in sandbox.evernote.com), add a config named `service_host` in the ini file as following:
```
[secret]
token = [encrypted token]
service_host = www.evernote.com
# For 印象笔记 users uncomment this line instead
# service_host = app.yinxiang.com
```

I made this process complicated just to warn you that this program although tested to work in my case but is not against all, including any special/corrupted/complicated notes. If this program corrupted your note, just *USE THE `-r` FLAG* below to **restore internal backups**! This is proved to be safe.

## Swap between block styles
Use `-t` `-c` or `-f`(currently not implemented) to batch replace blocks. If none of the three is indicated, this part will be skipped.

## Forbit edits

Official Mac client has known issues to scramble lines or styles of transformed code blocks. *I promise my code is always tested before pushed!* Meanwhile, Evernote API enforced a DTD check upon third party editing, that is, for a valid ENML markup, the disrupted format is definitely *caused by Evernote client*. If you encountered the same problem, just use `-k` to lock down the note and prevent Evernote entering edit mode, and open an issue if you are willing to solve it, thanks!

This utility can be used solely for note locking as well ;-)

# Commandline Reference
```
usage: run.py [-h] [-t] [-c] [-f] [-k] [-u] [-r]

optional arguments:
  -h, --help     show this help message and exit
  -t, --tag      Turn codeblocks to simple non-framed <pre> tag
  -c, --classic  Turn codeblocks to CLASSIC Evernote styles
  -f, --fancy    Turn codeblocks to FANCY highlighted styles[TODO]
  -k, --lock     Mark selected notes read-only
  -u, --unlock   Grant r/w permissions again
  -r, --restore  Restore notes to original states
```
