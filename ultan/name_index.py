from contextlib import contextmanager
import logging
import os

from .compat import redirect_stderr, redirect_stdout
from .strategies import ast_walker, sys_modules_scanner

_cache = None

log = logging.getLogger()


@contextmanager
def _squash_output(enabled=True):
    """Context manager that directs stderr and stdout to devnull.

    Args:
      enabled: If `True`, redirect output. Otherwise, do nothing.
    """
    if enabled:
        with open(os.devnull, mode='wt') as devnull,\
             redirect_stderr(devnull),\
             redirect_stdout(devnull):
            yield
    else:
        yield


def _find_all_names():
    """Find all names in the Python environment.
    """
    with _squash_output(False):
        yield from ast_walker.get_names()
        yield from sys_modules_scanner.get_names()


class NameIndex:
    """An index of all available names in the Python environment.
    """
    def __init__(self):
        self._name_cache = None

    def get_names(self, pattern=''):
        """Get all names that contain `pattern`.
        """
        return (name
                for name in self._cache
                if pattern in name)

    def clear_cache(self):
        """Clear the internal cache of name.

        This is useful to clean up space or force recalculation of the cache.
        """
        self._name_cache = None

    @property
    def _cache(self):
        if self._name_cache is None:
            self._name_cache = set(_find_all_names())
        return self._name_cache