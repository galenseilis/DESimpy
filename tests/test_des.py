import operator
from unittest.mock import Mock
from desimpy.des import Event, EventScheduler, stop_at_max_time_factory

def test_event_initialization():
    action = Mock()
    context = {"key": "value"}
    event = Event(time=5.0, action=action, context=context)

    assert event.time == 5.0
    assert event.action == action
    assert event.context == context
    assert event.active is True

def test_activate_deactivate():
    action = Mock()
    event = Event(time=5.0, action=action, context={})

    event.deactivate()
    assert event.active is False

    event.activate()
    assert event.active is True

def test_run_active_event():
    action = Mock(return_value="log_entry")
    context = {"key": "value"}
    event = Event(time=5.0, action=action, context=context)

    result = event.run()
    assert result == (5.0, "log_entry", context)
    action.assert_called_once_with(context)

def test_run_inactive_event():
    action = Mock(return_value="log_entry")
    context = {"key": "value"}
    event = Event(time=5.0, action=action, context=context)
    event.deactivate()

    result = event.run()
    assert result == (5.0, None, context)
    action.assert_not_called()

def test_scheduler_initialization():
    scheduler = EventScheduler()
    assert scheduler.current_time == 0
    assert scheduler.event_queue == []

def test_schedule_event():
    scheduler = EventScheduler()
    action = Mock()
    event = Event(time=5.0, action=action, context={})

    scheduler.schedule(event)
    assert len(scheduler.event_queue) == 1
    assert scheduler.event_queue[0] == (5.0, event)

def test_run_scheduler():
    scheduler = EventScheduler()
    action1 = Mock(return_value="log1")
    action2 = Mock(return_value="log2")
    event1 = Event(time=1.0, action=action1, context={})
    event2 = Event(time=2.0, action=action2, context={})

    scheduler.schedule(event1)
    scheduler.schedule(event2)

    stop = stop_at_max_time_factory(scheduler, max_time=2.0)
    scheduler.run(stop)

    assert scheduler.current_time == 2.0
    action1.assert_called_once()
    action2.assert_called_once()

def test_stop_at_max_time_factory():
    scheduler = EventScheduler()
    stop = stop_at_max_time_factory(scheduler, max_time=10.0)

    assert stop() is False
    scheduler.current_time = 10.0
    assert stop() is True

