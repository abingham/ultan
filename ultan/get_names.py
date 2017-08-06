# Get all root modules: IPython.core.completerlib.get_root_modules()
# Given a module name, find all submodules and attributes: IPython.core.compleeterlib.try_import(<module name>)
# https://docs.python.org/3/library/importlib.html#checking-if-a-module-can-be-imported

from collections import deque
import importlib
from importlib.util import find_spec, module_from_spec
import IPython.core.completerlib as clib
from itertools import islice

_cache = None


def _get_import_spec(name):
    try:
        return find_spec(name)
    except:
        # Hack: sometimes this throw attribute for no good reason. e.g. find_spec('http.cookies._Translator')
        # This also throws other crazy exceptions sometimes. Just roll with it.
        # TODO: Probably report a bug againt cpython
        return None

def _walk_namespace(root_names=None):
    cache = set()

    root_names = root_names or clib.get_root_modules()
    objs = deque((name, None, None) for name in root_names)

    while objs:
        name, base_obj, base_name = objs.popleft()

        print(name, base_name)

        if base_obj is None:
            # With no base object, we assume the name refers to a module.
            # (global objects will get picked up in 'builtins').

            # import the module
            try:
                obj = importlib.import_module(name)
            except:
                # Some modules try to sys-exit or other zany things when you import them...
                continue

            if id(obj) in cache:
                continue

            # Enqueue each of its submodule and attribute names into objs
            for subname in clib.try_import(name, False):
                objs.append((subname, obj, name))

            cache.add(id(obj))
            yield name

        else:
            assert base_name

            full_name = '{}.{}'.format(base_name, name)

            import_spec = _get_import_spec(full_name)
            if import_spec:
                try:
                    obj = importlib.import_module(full_name)
                except:
                    # see above...
                    continue

                if id(obj) in cache:
                    continue

                for subname in clib.try_import(full_name):
                    objs.append((subname, obj, full_name))

                cache.add(id(obj))
                yield full_name
            else:
                obj = getattr(base_obj, name)
                if id(obj) in cache:
                    continue
                cache.add(id(obj))
                yield full_name

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
        _cache = _walk_namespace()


def get_names(pattern):
    _ensure_cache()

    return (name
            for name in _cache
            if pattern in name)

# print(list(islice(_walk_namespace(), 1000)))
for name in _walk_namespace():
    print(name)
