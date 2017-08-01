from aiohttp import web
from functools import wraps
from .get_doc import get_doc


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


def main():
    app = web.Application()
    # app.router.add_get('/', handle)
    app.router.add_get('/get_doc', handle_get_doc)

    web.run_app(app, port=8080)


if __name__ == '__main__':
    main()
