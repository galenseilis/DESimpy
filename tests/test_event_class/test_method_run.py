import heapq
import pytest
from desimpy import Event, EventScheduler


def test_no_action():
    event = Event(2018)
    result = event.run()
    assert result is None


def test_lambda_none():
    event = Event(2018, action=lambda: None)
    result = event.run()
    assert result is None


def test_action_returns_literal():
    value = "foo"
    event = Event(2018, action=lambda: value)
    result = event.run()
    assert result == value


def test_event_timeout_event():
    env = EventScheduler()

    time1 = 2
    action1 = lambda: env.timeout(30)
    event1 = Event(time1, action1)

    env.schedule(event1)
    event_log = env.run_until_max_time(100)
    assert len(event_log) == 2
    assert event_log[0][0] == event1
    assert event_log[0][1] == None
    assert event_log[1][0].time == 32
    assert event_log[1][1] == None
