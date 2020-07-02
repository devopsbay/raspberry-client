import pytest
from aiohttp import web

from nfcclient.http_server import aiohttp_server

pytestmark = pytest.mark.asyncio


async def test_http_server(aiohttp_client):
    async def hello(request):
        return web.Response(text='Hello, world')

    app = web.Application()
    app.router.add_get("/", hello)
    await aiohttp_server(app, "localhost", 5555)
    client = await aiohttp_client(app)
    resp = await client.get('/')
    assert resp.status == 200
