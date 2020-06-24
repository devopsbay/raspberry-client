from nfcclient.doors.manager import DoorManager


def test_configure():
    dm = DoorManager()
    dm.configure([{"name": "100", "pin_id": 21}])
    assert len(dm._doors) == 1
    assert dm._doors["100"].pin_id == 21


def test_reconfigure():
    dm = DoorManager()
    dm.configure([{"name": "100", "pin_id": 21}, {"name": "101", "pin_id": 22}])
    assert len(dm._doors) == 2
    assert dm._doors["100"].pin_id == 21

    dm.configure([{"name": "102", "pin_id": 23}])
    assert len(dm._doors) == 1
    assert dm._doors["102"].pin_id == 23


def test_open_door_failed(caplog, event_loop):
    DoorManager().get("100")
    assert "No door with name: 100" in caplog.text

