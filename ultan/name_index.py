from contextlib import contextmanager
from multiprocessing import Queue
from queue import Empty
import logging
import os

from .compat import redirect_stderr, redirect_stdout
from .strategies import ast_walker, sys_modules_scanner
from multiprocessing import Process

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
        for strategy in (ast_walker.ASTWalkerStrategy(),
                         sys_modules_scanner.SysModulesStrategy()):
            yield from strategy.get_names()


def _find_and_enqueue_names(queue):
    """Fetch all of the names in the environment and put the results into `queue`.
    """
    names = list(_find_all_names())
    queue.put(names)


class NameIndex:
    """An index of all available names in the Python environment.
    """
    def __init__(self, build_cache=True):
        self._name_cache = None

        self._queue = Queue()
        if build_cache:
            self.rebuild_cache()

    @property
    def ready(self):
        """Indicates if the index has been built.

        It can take some time to build the name index, a process that happens
        asynchronously. This indicates if the index has been built and, thus,
        if the `NameIndex` is able to give results.
        """

        # First see if there are any new caches in the queue. If so, the last
        # of these (the last enqueued, not necessarily the last requested)
        # becomes the new cache.
        try:
            while True:
                self._name_cache = self._queue.get_nowait()
        except Empty:
            pass

        return self._name_cache is not None

    def get_names(self, pattern=''):
        """Get all names that start with `pattern`.

        Return: An iterable of `(name, module-name)` tuples where each `name`
            matches `pattern`. These tuples are not guaranteed to be unique. If
            the index is not `ready`, then this will return an empty iterable.
        """
        if not self.ready:
            return ()

        return ((name, module_name)
                for (name, module_name) in self._name_cache
                if pattern in name)

    def clear_cache(self):
        """Clear the internal cache of name.

        This is useful to clean up space or force recalculation of the cache.
        """
        self._name_cache = None

    def rebuild_cache(self):
        p = Process(target=_find_and_enqueue_names,
                    args=(self._queue,),
                    daemon=True)
        p.start()
