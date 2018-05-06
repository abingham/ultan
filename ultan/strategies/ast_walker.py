# A strategy for finding names that uses `pkgutil.walk_packages` and AST
# inspection.
#
# We use `pkgutil` to find modules. Then for every module, we look for its
# source code, build an AST, and look for names in the AST.
#
# This allows us to find names for modules without even importing them.

import ast
import logging
import pkgutil
from functools import singledispatch
from importlib.machinery import FileFinder
from zipimport import zipimporter, ZipImportError

from ultan.strategies.strategy import Strategy


log = logging.getLogger()


def _find_top_level_ast_names(module_node):
    """Search an AST for names.

    `tree` is assumed to be a Module.

    Returns: An iterable of names found in the module.
    """
    assert isinstance(module_node, ast.Module)

    for node in module_node.body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if hasattr(target, 'id'):
                    yield target.id
        elif isinstance(node, ast.FunctionDef):
            yield node.name
        elif isinstance(node, ast.ClassDef):
            yield node.name
        # TODO: nested stuff


@singledispatch
def _get_source(finder, module_name):
    """Get the source code for `module_name` via its finder.

    Returns: The source code for the module, or None if the source can't be
      found.
    """
    log.info('unsupported finder type %s for module %s', finder, module_name)
    return None


@_get_source.register(FileFinder)
def _(finder, module_name):
    """Get source for a module imported via a FileFinder.
    """
    spec = finder.find_spec(module_name)
    try:
        with open(spec.origin, mode='rt') as handle:
            return handle.read()
    except OSError:
        return None
    except UnicodeDecodeError:
            log.info('unicode decode error: %s', spec.origin)


@_get_source.register(zipimporter)
def _(finder, module_name):
    """Get the source for a modules imported via a zipimporter.
    """
    try:
        source = finder.get_source(module_name)
    except ZipImportError:
        log.info('could not find module %s in archive %s',
                 module_name,
                 finder.archive)
        return None

    if source is None:
        log.info('no source for module %s in archive %s',
                 module_name,
                 finder.archive)

    return source


class ASTWalkerStrategy(Strategy):
    def get_names(self):
        """Get an iterable of all names that can be found.
        """
        for minfo in pkgutil.walk_packages():
            finder, module_name, ispkg = minfo

            source = _get_source(finder, module_name)

            if source is None:
                log.info('no source found for module %s', module_name)
                continue

            try:
                tree = ast.parse(source)
                for name in _find_top_level_ast_names(tree):
                    yield (name, module_name)
            except SyntaxError:
                log.info('syntax error in module %s', name)
