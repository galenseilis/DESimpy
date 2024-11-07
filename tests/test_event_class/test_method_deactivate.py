from desimpy import Event, EventStatus


def test_deactivate_new():
    event = Event(2018)
    event.deactivate()
    assert event.status == EventStatus.INACTIVE


def test_already_inactive_manually():
    event = Event(2018)
    event.status = EventStatus.INACTIVE
    event.deactivate()
    assert event.status == EventStatus.INACTIVE
