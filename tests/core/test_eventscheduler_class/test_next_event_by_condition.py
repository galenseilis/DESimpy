from desimpy import Event, EventScheduler


def test_next_by_time():
    event0 = Event(-1)
    event1 = Event(0)
    event2 = Event(1)

    env = EventScheduler()

    env.schedule(event0)
    env.schedule(event1)
    env.schedule(event2)

    # NOTE: Cases related to t=-1
    assert env.next_event_by_condition(lambda env, event: event.time < -1) is None
    assert env.next_event_by_condition(lambda env, event: event.time <= -1) == event0
    assert env.next_event_by_condition(lambda env, event: event.time == -1) == event0
    assert env.next_event_by_condition(lambda env, event: event.time >= -1) == event0
    assert env.next_event_by_condition(lambda env, event: event.time > -1) is event1

    # NOTE: Cases related to t=0
    assert env.next_event_by_condition(lambda env, event: event.time < 0) is event0
    assert env.next_event_by_condition(lambda env, event: event.time <= 0) == event0
    assert env.next_event_by_condition(lambda env, event: event.time == 0) == event1
    assert env.next_event_by_condition(lambda env, event: event.time >= 0) == event1
    assert env.next_event_by_condition(lambda env, event: event.time > 0) is event2

    # NOTE: Cases related to t=1
    assert env.next_event_by_condition(lambda env, event: event.time < 1) is event0
    assert env.next_event_by_condition(lambda env, event: event.time <= 1) == event0
    assert env.next_event_by_condition(lambda env, event: event.time == 1) == event2
    assert env.next_event_by_condition(lambda env, event: event.time >= 1) == event2
    assert env.next_event_by_condition(lambda env, event: event.time > 1) is None


def test_next_by_if_action():
    event0 = Event(0, action=None)
    event1 = Event(0, action=lambda: None)
    event2 = Event(0, action=lambda: 2018)

    env = EventScheduler()

    env.schedule(event0)
    env.schedule(event1)
    env.schedule(event2)

    condition0 = lambda env, event: event.action() is None
    assert condition0(env, event0) == True
    assert condition0(env, event1) == True
    assert condition0(env, event2) == False
    assert env.next_event_by_condition(condition0) == event0

    condition1 = lambda env, event: event.action() == 2018
    assert condition1(env, event0) == False
    assert condition1(env, event1) == False
    assert condition1(env, event2) == True
    assert env.next_event_by_condition(condition1) == event2

    condition2 = lambda env, event: event.action == 2018
    assert condition2(env, event0) == False
    assert condition2(env, event1) == False
    assert condition2(env, event2) == False
    assert env.next_event_by_condition(condition2) is None


# TODO: Add more test cases...
