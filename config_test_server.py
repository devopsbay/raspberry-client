from aiohttp import web

routes = web.RouteTableDef()


@routes.get("/config/1")
async def config(request):
    return web.json_response({
        "master_keys": ["0x2b0x150x270xc", "0xda0x130x640x1a", "0xca0xbf0x570x1a", "0xa0x720xa90x15"],
        "doors": [
            {"name": "103", "pin_id": 21, "readers": ["D23", "D24"]},
            {"name": "101", "pin_id": 20, "readers": ["D22", "D27"]},
        ],
        "door_open_seconds": 1,
    })


app = web.Application()
app.add_routes(routes)
web.run_app(app=app, port=8080)
