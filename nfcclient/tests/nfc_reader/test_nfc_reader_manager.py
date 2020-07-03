from nfcclient.config import Door
from nfcclient.nfc_reader.nfc_reader import NFCReader


def test_configure(nfc_reader_manager):
    nfc_reader_manager.configure([Door(name="100", pin_id=21, readers=["D8"])])
    assert len(nfc_reader_manager._nfc_readers) == 1
    assert nfc_reader_manager._nfc_readers["D8"].door == "100"


def test_configure_fails(nfc_reader_manager, mocker, caplog):
    mocker.patch("nfcclient.nfc_reader.nfc_reader_factory.NFCReaderFactory.create").side_effect = Exception("LOL")
    nfc_reader_manager.configure([Door(name="100", pin_id=21, readers=["D8"])])
    assert "NFC Reader D8 for door 100 failed: LOL" in caplog.text


def test_reconfigure(nfc_reader_manager):
    nfc_reader_manager.configure([
        Door(name="100", pin_id=21, readers=["D8", "D10"]),
        Door(name="101", pin_id=22, readers=["D9"])
    ])
    assert len(nfc_reader_manager._nfc_readers) == 3
    assert nfc_reader_manager._nfc_readers["D10"].door == "100"

    nfc_reader_manager.configure([Door(name="102", pin_id=23, readers=["D9", "D20"])])
    assert len(nfc_reader_manager._nfc_readers) == 2
    assert nfc_reader_manager._nfc_readers["D9"].door == "102"


def test_all(nfc_reader_manager):
    nfc_reader_manager.configure([Door(name="lol", pin_id=21, readers=["D9"])])
    nfc_readers = nfc_reader_manager.all()
    assert len(nfc_readers) == 1
    assert nfc_readers[0].door == "lol"


def test_all_immutable(nfc_reader_manager):
    door = Door(name="lol", pin_id=21, readers=["D9"])
    nfc_reader_manager.configure([door])
    nfc_readers = nfc_reader_manager.all()
    assert len(nfc_readers) == 1
    assert nfc_readers[0].door == "lol"

    nfc_readers.append(NFCReader(pin="22", door="101", reader_timeout=1))
    assert len(nfc_readers) == 2
    assert len(nfc_reader_manager.all()) == 1


def test_all_by_door_name(nfc_reader_manager):
    nfc_reader_manager.configure([
        Door(name="lol", pin_id=21, readers=["D9", "D19"]),
        Door(name="lol1", pin_id=22, readers=["D10", "D21"]),
        Door(name="lol2", pin_id=23, readers=["D1", "D2"]),
    ])
    nfc_readers = nfc_reader_manager.all_by_door_name(door_name="lol1")
    assert len(nfc_readers) == 2
    assert nfc_readers[0].door == "lol1"
    assert nfc_readers[0].pin_number == "D10"
    assert nfc_readers[1].door == "lol1"
    assert nfc_readers[1].pin_number == "D21"
