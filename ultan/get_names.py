# Get all root modules: IPython.core.completerlib.get_root_modules()
# Given a module name, find all submodules and attributes: IPython.core.compleeterlib.try_import(<module name>)
# https://docs.python.org/3/library/importlib.html#checking-if-a-module-can-be-imported

from collections import deque
import importlib
from importlib.util import find_spec, module_from_spec
import IPython.core.completerlib as clib

_cache = None


def _walk_namespace(root_names=None):
    root_names = root_names or clib.get_root_modules()
    objs = deque((name, None, None) for name in root_names)

    while objs:
        name, base_obj, base_name = objs.pop()
        print('popped', name, base_obj, base_name)

        if base_obj is None:
            # With no base object, we assume the name refers to a module.
            # (global objects will get picked up in 'builtins').

            # import the module
            obj = importlib.import_module(name)

            # Enqueue each of its submodule and attribute names into objs
            for subname in clib.try_import(name, False):
                print('appending', subname, obj, name)
                objs.append((subname, obj, name))

            yield name

        else:
            assert base_name

            full_name = '{}.{}'.format(base_name, name)

            print('finding spec', full_name)
            import_spec = find_spec(full_name)
            if import_spec:
                obj = module_from_spec(import_spec)
                for subname in clib.try_import(full_name):
                    objs.append((subname, obj, full_name))

            # print('is importable?', base_obj, name)
            # if clib.is_importable(base_obj, name, True):
            #     print('importing', name, base_obj)
            #     obj = importlib.import_module(full_name)
            #     for subname in clib.try_import(full_name, True):
            #         print('> appending', subname, object, full_name)
            #         objs.append((subname, obj, full_name))
            #     yield full_name
            # else:
            #     obj = getattr(base_obj, name)


def _ensure_cache():
    global _cache
    if _cache is None:
        _cache = list(_walk_namespace())


def get_names(pattern):
    _ensure_cache()

    return (name
            for name in _cache
            if pattern in name)

print(list(_walk_namespace(['http'])))
