import ast
from contextlib import redirect_stderr, redirect_stdout
import logging
import os
import pkgutil

_cache = None

log = logging.getLogger()


def _find_top_level_names(tree):
    assert isinstance(tree, ast.Module)
    for node in tree.body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if hasattr(target, 'id'):
                    yield target.id
        elif isinstance(node, ast.FunctionDef):
            yield node.name
        # TODO: classes, nested stuff


def _walk_namespace():
    with open(os.devnull, mode='wt') as devnull,\
         redirect_stderr(devnull),\
         redirect_stdout(devnull):
        for minfo in pkgutil.walk_packages():
            spec = minfo.module_finder.find_spec(minfo.name)
            try:
                with open(spec.origin, mode='rt') as handle:
                    source = handle.read()
                tree = ast.parse(source)
                for name in _find_top_level_names(tree):
                    yield '{}.{}'.format(minfo.name, name)
            except UnicodeDecodeError:
                log.info('unicode decode error: %s', spec.origin)
            except SyntaxError:
                log.info('syntax error: %s', spec.origin)


def _ensure_cache():
    global _cache
    if _cache is None:
        _cache = list(_walk_namespace())


def get_names(pattern):
    _ensure_cache()

    return (name
            for name in _cache
            if pattern in name)

# _walk_namespace()
