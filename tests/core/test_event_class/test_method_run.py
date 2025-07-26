from desimpy import Event, EventScheduler
from desimpy.core import Simulation


def test_no_action():
    event = Event(2018)
    returned_result = event.run()
    assert event.result is None
    assert returned_result is None


def test_lambda_none():
    event = Event(2018, action=lambda: None)
    result = event.run()
    assert result is None
    assert event.result is None


def test_action_returns_literal():
    value: str = "foo"
    event = Event(2018, action=lambda: value)
    returned_result = event.run()
    assert event.result == value
    assert returned_result is None


def test_event_timeout_event():
    simulation = Simulation()

    time1 = 2
    action1 = lambda: simulation.scheduler.timeout(30)
    event1 = Event(time1, action1)

    simulation.scheduler.schedule(event1)
    event_log = simulation.run_until_max_time(100)
    assert len(event_log) == 2
    assert event_log[0] == event1
    assert event1.result == None
    assert event_log[1].time == 32
    assert event_log[1].result == None
