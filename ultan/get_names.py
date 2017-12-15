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
    with _squash_output(False):
        yield from ast_walker.get_names()
        yield from sys_modules_scanner.get_names()


def _ensure_cache():
    global _cache
    if _cache is None:
        _cache = list(_find_all_names())


def clear_cache():
    global _cache
    _cache = None


def get_names(pattern=''):
    _ensure_cache()

    return (name
            for name in _cache
            if pattern in name)
