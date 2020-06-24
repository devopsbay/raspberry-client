from nfcclient.api import refresh, open_door, index
from nfcclient.websocket_handler import websocket_handler

routes = [
    ('GET', '/', index, 'main'),
    ('GET', '/ws', websocket_handler, 'ws'),
    ('GET', '/refresh/', refresh, 'refresh'),
    ('GET', '/doors/{door_name}/open/', open_door, 'open_door'),
]
