from nfcclient.config import Door
from nfcclient.doors.manager import DoorManager


def test_configure():
    dm = DoorManager()
    dm.configure([Door(name="100", pin_id=21, readers=[])])
    assert len(dm._doors) == 1
    assert dm._doors["100"].pin_id == 21


def test_reconfigure():
    dm = DoorManager()
    dm.configure([Door(name="100", pin_id=21, readers=[]), Door(name="101", pin_id=22, readers=[])])
    assert len(dm._doors) == 2
    assert dm._doors["100"].pin_id == 21

    dm.configure([Door(name="102", pin_id=23, readers=[])])
    assert len(dm._doors) == 1
    assert dm._doors["102"].pin_id == 23


def test_open_door_failed(caplog, event_loop):
    DoorManager().get("100")
    assert "No door with name: 100" in caplog.text


def test_get(door_manager):
    door_manager.configure([Door(name="lol", pin_id=21, readers=[])])
    door = door_manager.get("lol")
    assert door.name == "lol"
    assert door.pin_id == 21


def test_all(door_manager):
    door_manager.configure([Door(name="lol", pin_id=21, readers=[])])
    doors = door_manager.all()
    assert len(doors) == 1
    assert doors[0].name == "lol"
    assert doors[0].pin_id == 21


def test_all_immutable(door_manager):
    door = Door(name="lol", pin_id=21, readers=[])
    door_manager.configure([door])
    doors = door_manager.all()
    assert len(doors) == 1
    assert doors[0].name == "lol"
    assert doors[0].pin_id == 21

    doors.append(door)
    assert len(doors) == 2
    assert len(door_manager.all()) == 1


def test_all_by_not_opened(door_manager):
    door_manager.configure([
        Door(name="lol", pin_id=21, readers=[]),
        Door(name="lol2", pin_id=22, readers=[]),
    ])
    doors = door_manager.all()
    assert len(doors) == 2

    doors[0]._opened = True

    doors_not_opened = door_manager.all_by_not_opened()
    assert len(doors_not_opened) == 1
    assert doors_not_opened[0].name == "lol2"
    assert doors_not_opened[0].pin_id == 22

