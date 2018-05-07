import sys
from time import sleep

import docopt_subcommands as dsc

from . import version
from .name_index import NameIndex
from ultan.get_doc import get_doc


@dsc.command()
def names_handler(args):
    """usage: {program} names <pattern>

    List names (and modules) matching the pattern.
    """
    index = NameIndex()

    while not index.ready:
        sleep(0.1)

    for (name, module_name) in index.get_names(args['<pattern>']):
        print('{} [in {}]'.format(name, module_name))


@dsc.command()
def doc_handler(args):
    """usage: {program} doc <name>

    Get the docstring for a Python object.
    """
    print(get_doc(args['<name>']))


def main(args=None):
    if args is None:
        args = sys.argv[1:]

    return dsc.main(
        program='ultan',
        version='ultan v{}'.format(version.__version__),
        argv=args
    )


if __name__ == '__main__':
    sys.exit(main())
