import builtins
from functools import reduce
import importlib
from itertools import accumulate


def find_module(full_name):
    module = builtins
    module_name = ''

    names = filter(
        None,
        accumulate(
            full_name.split('.'),
            lambda acc, n: '{}.{}'.format(acc, n)))

    for name in names:
        try:
            module = importlib.import_module(name)
            module_name = name
        except ModuleNotFoundError:
            break

    return (module, module_name)


def find_object(module, name):
    names = filter(None, name.split('.'))
    return reduce(getattr, names, module)


def get_doc(full_name):
    module, module_name = find_module(full_name)

    assert full_name.startswith(module_name)

    obj_name = full_name[len(module_name):]
    try:
        obj = find_object(module, obj_name)
    except AttributeError:
        raise ValueError('No object with name {}'.format(full_name))

    return obj.__doc__
