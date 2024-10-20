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
    value = 'foo'
    event = Event(2018, action=lambda: value)
    result = event.run()
    assert result == value

def test_event_that_times_out_event():
    env = EventScheduler()

    time1 = 2
    action1 = lambda: env.timeout(30)
    event1 = Event(time1, action1)

    env.schedule(event1)
    event1.run()
    
    assert len(env.event_queue) == 2
    assert env.next_event() == event1
    step1 = env.step()
    assert step1[0].time == 2
    step2 = env.step()
    assert step2[0].time == 30
    assert step2[1] == None

    # WARN: Not sure if this last event should exist.
    step3 = env.step()
    assert step3[0].time == 32
    assert step3[1] == None
