from argparse import ArgumentParser
import sys


_parser = ArgumentParser()
_parser.add_argument("-t", "--tag", action="store_true",
                     help="Turn codeblocks to simple non-framed <pre> tag")
_parser.add_argument("-c", "--classic", action="store_true",
                     help="Turn codeblocks to CLASSIC Evernote styles")
_parser.add_argument("-f", "--fancy", action="store_true",
                     help="Turn codeblocks to FANCY highlighted styles[TODO]")
_parser.add_argument("-k", "--lock", action="store_true",
                     help="Mark selected notes read-only")
_parser.add_argument("-u", "--unlock", action="store_true",
                     help="Grant r/w permissions again")
_parser.add_argument("-r", "--restore", action="store_true",
                     help="Restore notes to original states")


def get_args(args=None):
    if len(sys.argv) == 1:
        _parser.print_help()
        raise SystemExit
    return _parser.parse_args(args)
