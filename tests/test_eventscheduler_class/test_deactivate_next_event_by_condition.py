from desimpy import Event, EventScheduler, EventStatus

# Test Suite for deactivate_next_event_by_condition


def condition_example(scheduler: EventScheduler, event: Event):
    """Example condition function for testing."""
    return event.time < 10  # For testing, deactivate events with time < 10.


def test_deactivate_next_event_by_condition_empty_queue():
    """Test `deactivate_next_event_by_condition` with an empty event queue."""
    scheduler = EventScheduler()

    # Apply condition to deactivate events
    scheduler.deactivate_next_event_by_condition(condition_example)

    # Ensure the queue remains empty
    assert len(scheduler.event_queue) == 0, "The event queue should remain empty."


def test_deactivate_next_event_by_condition_single_event_no_match():
    """Test `deactivate_next_event_by_condition` with a single event that doesn't match the condition."""
    scheduler = EventScheduler()
    event1 = Event(time=15)

    # Schedule event1
    scheduler.schedule(event1)

    # Apply condition to deactivate events (event1 should not be deactivated since time > 10)
    scheduler.deactivate_next_event_by_condition(condition_example)

    # Ensure event1 is still active
    assert (
        event1.status == EventStatus.ACTIVE
    ), "Event1 should remain active as it doesn't meet the condition."


def test_deactivate_next_event_by_condition_single_event_match():
    """Test `deactivate_next_event_by_condition` with a single event that matches the condition."""
    scheduler = EventScheduler()
    event1 = Event(time=5)

    # Schedule event1
    scheduler.schedule(event1)

    # Apply condition to deactivate events (event1 should be deactivated since time < 10)
    scheduler.deactivate_next_event_by_condition(condition_example)

    # Ensure event1 is deactivated
    assert (
        event1.status == EventStatus.INACTIVE
    ), "Event1 should be deactivated as it meets the condition."


def test_deactivate_next_event_by_condition_multiple_events_some_match():
    """Test `deactivate_next_event_by_condition` with multiple events, some matching the condition."""
    scheduler = EventScheduler()
    event1 = Event(time=5)
    event2 = Event(time=15)
    event3 = Event(time=8)

    # Schedule the events
    scheduler.schedule(event1)
    scheduler.schedule(event2)
    scheduler.schedule(event3)

    # Apply condition to deactivate events (event1 and event3 should be deactivated since time < 10)
    scheduler.deactivate_next_event_by_condition(condition_example)

    # Ensure event1 and event3 are deactivated, and event2 remains active
    assert event1.status == EventStatus.INACTIVE, "Event1 should be deactivated."
    assert event2.status == EventStatus.ACTIVE, "Event2 should remain active."
    assert event3.status == EventStatus.ACTIVE, "Event3 should still be active."


def test_deactivate_next_event_by_condition_all_events_match():
    """Test `deactivate_next_event_by_condition` with multiple events, all matching the condition."""
    scheduler = EventScheduler()
    event1 = Event(time=5)
    event2 = Event(time=8)
    event3 = Event(time=3)

    # Schedule the events
    scheduler.schedule(event1)
    scheduler.schedule(event2)
    scheduler.schedule(event3)

    # Apply condition to deactivate next event meeting criterion.
    scheduler.deactivate_next_event_by_condition(condition_example)

    # Ensure all events are deactivated
    assert event1.status == EventStatus.ACTIVE, "Event1 should still be active."
    assert event2.status == EventStatus.ACTIVE, "Event2 should still be active."
    assert event3.status == EventStatus.INACTIVE, "Event3 should be deactivated."


def test_deactivate_next_event_by_condition_none_match():
    """Test `deactivate_next_event_by_condition` with multiple events, none matching the condition."""
    scheduler = EventScheduler()
    event1 = Event(time=15)
    event2 = Event(time=20)
    event3 = Event(time=30)

    # Schedule the events
    scheduler.schedule(event1)
    scheduler.schedule(event2)
    scheduler.schedule(event3)

    # Apply condition to deactivate events (none should be deactivated since time > 10)
    scheduler.deactivate_next_event_by_condition(condition_example)

    # Ensure no events are deactivated
    assert event1.status == EventStatus.ACTIVE, "Event1 should remain active."
    assert event2.status == EventStatus.ACTIVE, "Event2 should remain active."
    assert event3.status == EventStatus.ACTIVE, "Event3 should remain active."


def test_deactivate_next_event_by_condition_deactivate_one_at_a_time():
    """Test `deactivate_next_event_by_condition` to ensure only one event is deactivated at a time."""
    scheduler = EventScheduler()
    event1 = Event(time=5)
    event2 = Event(time=2)
    event3 = Event(time=15)

    # Schedule the events
    scheduler.schedule(event1)
    scheduler.schedule(event2)
    scheduler.schedule(event3)

    # Apply condition and deactivate events one by one
    scheduler.deactivate_next_event_by_condition(condition_example)
    _ = scheduler.run_until_max_time(4)
    scheduler.deactivate_next_event_by_condition(condition_example)

    # Ensure only event1 and event2 are deactivated, event3 remains active
    assert event1.status == EventStatus.INACTIVE, "Event1 should be deactivated."
    assert event2.status == EventStatus.INACTIVE, "Event2 should be deactivated."
    assert event3.status == EventStatus.ACTIVE, "Event3 should remain active."


def test_deactivate_next_event_by_condition_already_inactive():
    """Test `deactivate_next_event_by_condition` where the event is already inactive."""
    scheduler = EventScheduler()
    event1 = Event(time=5)
    event2 = Event(time=12)

    # Deactivate event1 manually
    event1.deactivate()

    # Schedule both events
    scheduler.schedule(event1)
    scheduler.schedule(event2)

    # Apply condition to deactivate events
    scheduler.deactivate_next_event_by_condition(condition_example)

    # Ensure event1 remains inactive and event2 is remains active.
    assert event1.status == EventStatus.INACTIVE, "Event1 should remain inactive."
    assert event2.status == EventStatus.ACTIVE, "Event2 should remain active."


def test_deactivate_next_event_by_condition_with_different_conditions():
    """Test `deactivate_next_event_by_condition` with different condition functions."""
    scheduler = EventScheduler()
    event1 = Event(time=5)
    event2 = Event(time=12)
    event3 = Event(time=8)

    # Define a different condition function
    def condition_other(scheduler: EventScheduler, event: Event):
        _ = scheduler
        return event.time == 8  # Only deactivate events with time == 8

    # Schedule the events
    scheduler.schedule(event1)
    scheduler.schedule(event2)
    scheduler.schedule(event3)

    # Apply the new condition to deactivate events
    scheduler.deactivate_next_event_by_condition(condition_other)

    # Ensure only event3 is deactivated
    assert event1.status == EventStatus.ACTIVE, "Event1 should remain active."
    assert event2.status == EventStatus.ACTIVE, "Event2 should remain active."
    assert event3.status == EventStatus.INACTIVE, "Event3 should be deactivated."
