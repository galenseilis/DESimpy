from desimpy import Event


def test_deactivate_new():
    event = Event(2018)
    event.deactivate()
    assert event.active == False


def test_already_inactive_manually():
    event = Event(2018)
    event.active = False
    event.deactivate()
    assert event.active == False
