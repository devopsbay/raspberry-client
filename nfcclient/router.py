from nfcclient.api import refresh, open_door, restart_readers, health_check

routes = [
    ('GET', '/', health_check, 'health'),
    ('GET', '/refresh/', refresh, 'refresh'),
    ('GET', '/restart_readers/', restart_readers, 'restart_readers'),
    ('GET', '/doors/{door_name}/open/', open_door, 'open_door'),
]
