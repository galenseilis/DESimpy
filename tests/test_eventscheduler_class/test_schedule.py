import pytest
from desimpy import Event, EventScheduler

def test_schedule_nonevent():
    class Foo:
        def __init__(self):
            self.time = 0

    env = EventScheduler()
    with pytest.raises(TypeError):
        env.schedule(Foo())


def test_schedule_int():
    env = EventScheduler()
    with pytest.raises(TypeError):
        env.schedule(int)

def test_schedule_str():
    env = EventScheduler()
    with pytest.raises(TypeError):
        env.schedule(str)

def test_schedule_negative_after_zero():
    env = EventScheduler()
    event1 = Event(10)
    event2 = Event(-10)
    env.schedule(event1)
    env.run_until_max_time(20)
    with pytest.raises(ValueError):
        env.schedule(event2)
