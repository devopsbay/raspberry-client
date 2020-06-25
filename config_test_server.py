from aiohttp import web

routes = web.RouteTableDef()


@routes.get("/config/1")
async def config(request):
    return web.json_response({
        "master_keys": ["0x2b0x150x270xc"],
        "doors": [
            {"name": "103", "pin_id": 21, "readers": ["D8"]},
        ],
        "door_open_seconds": 5,
    })


@routes.get("/auth/card/{card_id}/{door_name}")
async def config(request):
    if request.match_info["card_id"] == "0x170xff0x7a0x4b":
        return web.json_response({
            "status": True,
        })
    else:
        return web.json_response({
            "status": False,
        })


app = web.Application()
app.add_routes(routes)
web.run_app(app=app, port=8080)
