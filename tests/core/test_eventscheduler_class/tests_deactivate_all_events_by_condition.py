from desimpy import Event, Environment, EventStatus

# Test Suite for deactivate_all_events_by_condition


def condition_example(scheduler: Environment, event: Event):
    """Example condition function for testing."""
    _ = scheduler
    return event.time < 10  # For testing, deactivate events with time < 10.


def test_deactivate_all_events_by_condition_empty_queue():
    """Test `deactivate_all_events_by_condition` with an empty event queue."""
    scheduler = Environment()

    # Apply condition to deactivate all events
    scheduler.deactivate_all_events_by_condition(condition_example)

    # Ensure the queue remains empty
    assert len(scheduler.event_queue) == 0, "The event queue should remain empty."


def test_deactivate_all_events_by_condition_no_match():
    """Test `deactivate_all_events_by_condition` with events that don't match the condition."""
    scheduler = Environment()
    event1 = Event(time=15)
    event2 = Event(time=20)

    # Schedule the events
    scheduler.schedule(event1)
    scheduler.schedule(event2)

    # Apply condition to deactivate all events (none should be deactivated since time > 10)
    scheduler.deactivate_all_events_by_condition(condition_example)

    # Ensure no events are deactivated
    assert event1.status == EventStatus.ACTIVE, "Event1 should remain active."
    assert event2.status == EventStatus.ACTIVE, "Event2 should remain active."


def test_deactivate_all_events_by_condition_all_match():
    """Test `deactivate_all_events_by_condition` with events that all match the condition."""
    scheduler = Environment()
    event1 = Event(time=5)
    event2 = Event(time=8)
    event3 = Event(time=3)

    # Schedule the events
    scheduler.schedule(event1)
    scheduler.schedule(event2)
    scheduler.schedule(event3)

    # Apply condition to deactivate all events (all events should be deactivated since time < 10)
    scheduler.deactivate_all_events_by_condition(condition_example)

    # Ensure all events are deactivated
    assert event1.status == EventStatus.INACTIVE, "Event1 should be deactivated."
    assert event2.status == EventStatus.INACTIVE, "Event2 should be deactivated."
    assert event3.status == EventStatus.INACTIVE, "Event3 should be deactivated."


def test_deactivate_all_events_by_condition_some_match():
    """Test `deactivate_all_events_by_condition` with some events matching the condition."""
    scheduler = Environment()
    event1 = Event(time=5)
    event2 = Event(time=15)
    event3 = Event(time=8)

    # Schedule the events
    scheduler.schedule(event1)
    scheduler.schedule(event2)
    scheduler.schedule(event3)

    # Apply condition to deactivate all events (event1 and event3 should be deactivated since time < 10)
    scheduler.deactivate_all_events_by_condition(condition_example)

    # Ensure event1 and event3 are deactivated, and event2 remains active
    assert event1.status == EventStatus.INACTIVE, "Event1 should be deactivated."
    assert event2.status == EventStatus.ACTIVE, "Event2 should remain active."
    assert event3.status == EventStatus.INACTIVE, "Event3 should be deactivated."


def test_deactivate_all_events_by_condition_none_match():
    """Test `deactivate_all_events_by_condition` with no events matching the condition."""
    scheduler = Environment()
    event1 = Event(time=15)
    event2 = Event(time=20)
    event3 = Event(time=30)

    # Schedule the events
    scheduler.schedule(event1)
    scheduler.schedule(event2)
    scheduler.schedule(event3)

    # Apply condition to deactivate all events (none should be deactivated since time > 10)
    scheduler.deactivate_all_events_by_condition(condition_example)

    # Ensure no events are deactivated
    assert event1.status == EventStatus.ACTIVE, "Event1 should remain active."
    assert event2.status == EventStatus.ACTIVE, "Event2 should remain active."
    assert event3.status == EventStatus.ACTIVE, "Event3 should remain active."


def test_deactivate_all_events_by_condition_already_inactive():
    """Test `deactivate_all_events_by_condition` where some events are already inactive."""
    scheduler = Environment()
    event1 = Event(time=5)
    event2 = Event(time=12)
    event3 = Event(time=8)

    # Deactivate event2 manually
    event2.deactivate()

    # Schedule the events
    scheduler.schedule(event1)
    scheduler.schedule(event2)
    scheduler.schedule(event3)

    # Apply condition to deactivate all events (event1 and event3 should be deactivated)
    scheduler.deactivate_all_events_by_condition(condition_example)

    # Ensure event1 and event3 are deactivated, and event2 remains inactive
    assert event1.status == EventStatus.INACTIVE, "Event1 should be deactivated."
    assert event2.status == EventStatus.INACTIVE, "Event2 should remain inactive."
    assert event3.status == EventStatus.INACTIVE, "Event3 should be deactivated."


def test_deactivate_all_events_by_condition_multiple_conditions():
    """Test `deactivate_all_events_by_condition` with multiple conditions."""
    scheduler = Environment()
    event1 = Event(time=5)
    event2 = Event(time=12)
    event3 = Event(time=8)

    # Define a different condition function
    def condition_other(scheduler: Environment, event: Event):
        _ = scheduler
        return event.time == 8  # Only deactivate events with time == 8

    # Schedule the events
    scheduler.schedule(event1)
    scheduler.schedule(event2)
    scheduler.schedule(event3)

    # Apply the condition to deactivate events (only event3 should be deactivated)
    scheduler.deactivate_all_events_by_condition(condition_other)

    # Ensure only event3 is deactivated
    assert event1.status == EventStatus.ACTIVE, "Event1 should remain active."
    assert event2.status == EventStatus.ACTIVE, "Event2 should remain active."
    assert event3.status == EventStatus.INACTIVE, "Event3 should be deactivated."


def test_deactivate_all_events_by_condition_deactivate_one_at_a_time():
    """Test `deactivate_all_events_by_condition` to ensure only events that match are deactivated."""
    scheduler = Environment()
    event1 = Event(time=5)
    event2 = Event(time=15)
    event3 = Event(time=8)

    # Schedule the events
    scheduler.schedule(event1)
    scheduler.schedule(event2)
    scheduler.schedule(event3)

    # Apply condition and deactivate events one by one
    scheduler.deactivate_all_events_by_condition(condition_example)

    # Ensure event1 and event3 are deactivated, event2 remains active
    assert event1.status == EventStatus.INACTIVE, "Event1 should be deactivated."
    assert event2.status == EventStatus.ACTIVE, "Event2 should remain active."
    assert event3.status == EventStatus.INACTIVE, "Event3 should be deactivated."


def test_deactivate_all_events_by_condition_condition_function():
    """Test `deactivate_all_events_by_condition` with a custom condition function."""
    scheduler = Environment()

    def custom_condition(scheduler: Environment, event: Event):
        _ = scheduler
        return event.time > 10  # Deactivate events with time greater than 10.

    event1 = Event(time=5)
    event2 = Event(time=12)
    event3 = Event(time=20)

    # Schedule the events
    scheduler.schedule(event1)
    scheduler.schedule(event2)
    scheduler.schedule(event3)

    # Apply custom condition
    scheduler.deactivate_all_events_by_condition(custom_condition)

    # Ensure only event2 and event3 are deactivated
    assert event1.status == EventStatus.ACTIVE, "Event1 should remain active."
    assert event2.status == EventStatus.INACTIVE, "Event2 should be deactivated."
    assert event3.status == EventStatus.INACTIVE, "Event3 should be deactivated."
