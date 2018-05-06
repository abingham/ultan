# Find names by scanning modules in sys.modules.

import sys

from ultan.strategies.strategy import Strategy


class SysModulesStrategy(Strategy):
    def get_names(self):
        for module in list(sys.modules.values()):
            for name in module.__dict__:
                yield (name, module.__name__)
