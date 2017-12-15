"""ultan

A Python identifier and documentation server.

Usage:
  ultan [options]

Options:
  -h, --help          Show this screen.
  -p <P>, --port=<P>  The port on which ultan will listen [default: 0]
  -V, --version       Show version.
"""

from functools import wraps
import os
import sys

from aiohttp import web
import docopt

from .get_doc import get_doc
from .get_names import get_names
from .version import __version__


def json(f):
    @wraps(f)
    async def wrapper(*args, **kwargs):
        result = await f(*args, **kwargs)
        return web.json_response(result)
    return wrapper


@json
async def handle_get_doc(request):
    name = request.query['name']
    try:
        doc = get_doc(name)
    except ValueError:
        # TODO: Return 404 or something
        return 'not found'

    return doc


@json
async def handle_get_names(request):
    pattern = request.query['pattern']
    return list(get_names(pattern))


def main():
    args = docopt.docopt(__doc__, version='ultan {}'.format(__version__))

    try:
        port = int(args['--port'])
    except ValueError:
        print('Port must be a positive integer.', file=sys.stderr)
        return os.EX_CONFIG

    app = web.Application()
    app.router.add_get('/get_doc', handle_get_doc)
    app.router.add_get('/get_names', handle_get_names)

    return web.run_app(app, port=port)


if __name__ == '__main__':
    sys.exit(main())
