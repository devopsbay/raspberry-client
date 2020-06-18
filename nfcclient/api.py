import asyncio

from aiohttp import web

routes = web.RouteTableDef()


@routes.get("/refresh/")
async def refresh(request):
    request.app["config"].refresh_from_server()
    return web.json_response({"status": "ok"})


@routes.get("/doors/{door_name}/open/")
async def open_door(request):
    door_name = request.match_info["door_name"]
    gpio_client = request.app["config"].gpio_client
    seconds = int(request.rel_url.query.getone("seconds", gpio_client.door_open_seconds))
    asyncio.create_task(gpio_client.open_door(
        door_name=door_name,
        card_id="HUB",
        seconds=seconds,
    ))
    return web.json_response({"status": "ok"})

app = web.Application()
app.add_routes(routes)
