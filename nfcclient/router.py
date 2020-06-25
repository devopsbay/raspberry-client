from nfcclient.api import refresh, open_door

routes = [
    ('GET', '/refresh/', refresh, 'refresh'),
    ('GET', '/doors/{door_name}/open/', open_door, 'open_door'),
]
