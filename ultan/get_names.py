# Get all root modules: IPython.core.completerlib.get_root_modules()
# Given a module name, find all submodules and attributes: IPython.core.compleeterlib.try_import(<module name>)

import IPython.core.completerlib

_cache = None


def _build_cache():
    objs = IPython.core.completelib.get_root_modules()
    while objs:
        obj = objs[0]
        objs = objs[1:]

        yield obj


def get_names(pattern):
    if _cache is None:
        _build_cache()

    return (name
            for name in _cache
            if pattern in name)
