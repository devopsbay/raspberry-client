import asyncio
from aiohttp import web
import aiohttp_cors


async def handler(request):
    return web.Response(
        text="Hello!",
        )

#headers={"Access-Control-Request-Method": "GET",
        #    "Access-Control-Request-Headers": "Content-Type, x-requested-with", "Origin": "http://localhost:3001"
        #}

def setup_cors(app):
    resources = [
        'http://localhost:3001',
        'http://localhost:8080'
    ]

    cors = aiohttp_cors.setup(app, defaults={
        resource: aiohttp_cors.ResourceOptions(
            allow_credentials=True,
            expose_headers='*',
            allow_methods='*',
            allow_headers='*',
        ) for resource in resources
    })
    for route in app.router.routes():
        cors.add(route)

app = web.Application()

# `aiohttp_cors.setup` returns `aiohttp_cors.CorsConfig` instance.
# The `cors` instance will store CORS configuration for the
# application.
# Setup application routes.
app.router.add_route("GET", "/hello", handler)

cors = setup_cors(app)
# Configure default CORS settings.
# cors = aiohttp_cors.setup(app, defaults={
#     "http://localhost:3001": aiohttp_cors.ResourceOptions(
#             allow_credentials=True,
#             expose_headers="*",
#             allow_headers="*",
#         )
# })
#
# # Configure CORS on all routes.
# for route in list(app.router.routes()):
#     cors.add(route)


if __name__ == '__main__':
    web.run_app(app)