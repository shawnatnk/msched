from pprint import pprint
import sys


def d():
    sys.exit(0)


def p(s, title=None):
    if title:
        pprint("[{}]:".format(title))
    pprint(s, indent=4)
