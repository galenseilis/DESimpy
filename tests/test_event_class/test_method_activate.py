from desimpy import Event


def test_already_active():
    event = Event(2018)
    event.activate()
    assert event.active == True


def test_activate_manual_inactive():
    event = Event(2018)
    event.active = False
    event.activate()
    assert event.active == True


def test_activate_deactivated_event():
    event = Event(2018)
    event.deactivate()
    event.activate()
    assert event.active == True
