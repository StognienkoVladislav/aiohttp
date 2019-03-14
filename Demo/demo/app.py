from aiohttp import web


async def create_app():
    app = web.Application()
    return app
