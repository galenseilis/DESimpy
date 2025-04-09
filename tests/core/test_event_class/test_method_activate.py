from desimpy.core import Event, EventStatus


def test_already_active():
    event = Event(2018)
    event.activate()
    assert event.status == EventStatus.ACTIVE


def test_activate_manual_inactive():
    event = Event(2018)
    event.status = EventStatus.INACTIVE
    event.activate()
    assert event.status == EventStatus.ACTIVE


def test_activate_deactivated_event():
    event = Event(2018)
    event.deactivate()
    event.activate()
    assert event.status == EventStatus.ACTIVE
