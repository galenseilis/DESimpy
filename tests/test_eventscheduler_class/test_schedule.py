import pytest

from desimpy import Event, EventScheduler


def test_schedule_nonevent():
    class Foo:
        def __init__(self):
            self.time: int | float = 0

    env = EventScheduler()
    with pytest.raises(TypeError):
        env.schedule(Foo())


def test_schedule_int():
    env = EventScheduler()
    with pytest.raises(TypeError):
        env.schedule(2018)


def test_schedule_float():
    env = EventScheduler()
    with pytest.raises(TypeError):
        env.schedule(2018.0)


def test_schedule_str():
    env = EventScheduler()
    with pytest.raises(TypeError):
        env.schedule(str(2018))


def test_schedule_negative_time_when_active():
    env = EventScheduler()
    event = Event(-10)
    env._activate()
    with pytest.raises(ValueError):
        env.schedule(event)


# NOTE: Negative schedule times are allowed when simulation is inactive.
# NOTE: Allowing this case allows for state preparation before t=0.
def test_schedule_negative_time_when_inactive():
    env = EventScheduler()
    event = Event(-10)
    env.schedule(event)
    assert env.run_until_max_time(10)[0] == event


def test_event_with_context():
    time = 10
    action = lambda: 2018
    context = {"foo": "bar", 1: "baz"}
    event = Event(time, action, context)
    env = EventScheduler()
    env.schedule(event)
    event_out = env.step()
    assert event_out == event
    assert event_out.result == 2018
