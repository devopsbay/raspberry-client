from nfcclient.api import refresh, open_door, restart_readers

routes = [
    ('GET', '/refresh/', refresh, 'refresh'),
    ('GET', '/restart_readers/', restart_readers, 'restart_readers'),
    ('GET', '/doors/{door_name}/open/', open_door, 'open_door'),
]
