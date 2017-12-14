# Find names by scanning modules in sys.modules.

import sys


def get_names():
    for module in list(sys.modules.values()):
        for name in module.__dict__:
            yield '{}.{}'.format(module.__name__, name)
