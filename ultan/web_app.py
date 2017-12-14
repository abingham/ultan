from functools import wraps
import sys

from aiohttp import web

from .get_doc import get_doc
from .get_names import get_names


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
    app = web.Application()
    app.router.add_get('/get_doc', handle_get_doc)
    app.router.add_get('/get_names', handle_get_names)

    return web.run_app(app, port=12345)


if __name__ == '__main__':
    sys.exit(main())
