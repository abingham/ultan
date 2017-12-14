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


def get_names():
    for minfo in pkgutil.walk_packages():
        spec = minfo.module_finder.find_spec(minfo.name)
        try:
            with open(spec.origin, mode='rt') as handle:
                source = handle.read()
            tree = ast.parse(source)
            for name in _find_top_level_ast_names(tree):
                yield '{}.{}'.format(minfo.name, name)
        except UnicodeDecodeError:
            log.info('unicode decode error: %s', spec.origin)
        except SyntaxError:
            log.info('syntax error: %s', spec.origin)
