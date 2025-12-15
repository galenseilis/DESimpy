from desimpy.core import Event, Environment, EventStatus

# Test Suite for deactivate_next_event


def test_deactivate_next_event_empty_queue():
    """Test `deactivate_next_event` with an empty event queue."""
    scheduler = Environment()

    # Deactivate the next event when the queue is empty
    scheduler.deactivate_next_event()

    # Ensure no errors occurred and the queue remains empty
    assert len(scheduler.event_queue) == 0, "The event queue should remain empty."


def test_deactivate_next_event_single_event():
    """Test `deactivate_next_event` with a single event in the queue."""
    scheduler = Environment()
    event1 = Event(time=5)
    event1.deactivate()

    # Schedule the event and deactivate it
    scheduler.schedule(event1)
    scheduler.deactivate_next_event()

    # Ensure the event was deactivated
    assert event1.status == EventStatus.INACTIVE, (
        "Event1 should be deactivated after calling deactivate_next_event."
    )


def test_deactivate_next_event_multiple_events():
    """Test `deactivate_next_event` with multiple events in the queue."""
    scheduler = Environment()
    event1 = Event(time=5)
    event2 = Event(time=15)
    event3 = Event(time=25)

    # Schedule the events, all should be initially inactive
    event1.deactivate()
    event2.deactivate()
    event3.deactivate()
    scheduler.schedule(event1)
    scheduler.schedule(event2)
    scheduler.schedule(event3)

    # Deactivate the next event (event1 should be the first one)
    scheduler.deactivate_next_event()

    # Ensure the first event (event1) is deactivated, others remain active
    assert event1.status == EventStatus.INACTIVE, "Event1 should be deactivated."
    assert event2.status == EventStatus.INACTIVE, (
        "Event2 should remain inactive as it's not the next event."
    )
    assert event3.status == EventStatus.INACTIVE, (
        "Event3 should remain inactive as it's not the next event."
    )


def test_deactivate_next_event_with_already_inactive_event():
    """Test `deactivate_next_event` when the next event is already inactive."""
    scheduler = Environment()
    event1 = Event(time=5)
    event2 = Event(time=10)

    # Deactivate event1 manually and then schedule both events
    event1.deactivate()
    event2.deactivate()
    scheduler.schedule(event1)
    scheduler.schedule(event2)

    # Deactivate the next event (event1 should be the first one)
    scheduler.deactivate_next_event()

    # Ensure event1 stays inactive and event2 becomes inactive as it's the next event to deactivate
    assert event1.status == EventStatus.INACTIVE, "Event1 should remain inactive."
    assert event2.status == EventStatus.INACTIVE, (
        "Event2 should become inactive after calling deactivate_next_event."
    )


def test_deactivate_next_event_multiple_deactivations():
    """Test `deactivate_next_event` with multiple consecutive deactivations."""
    scheduler = Environment()
    event1 = Event(time=5)
    event2 = Event(time=10)
    event3 = Event(time=15)

    # Deactivate events manually and schedule them
    event1.deactivate()
    event2.deactivate()
    event3.deactivate()
    scheduler.schedule(event1)
    scheduler.schedule(event2)
    scheduler.schedule(event3)

    # Deactivate the next event, twice (it should deactivate event1, then event2)
    scheduler.deactivate_next_event()
    scheduler.deactivate_next_event()

    # Ensure event1 and event2 are deactivated, but event3 remains active
    assert event1.status == EventStatus.INACTIVE, "Event1 should be deactivated."
    assert event2.status == EventStatus.INACTIVE, "Event2 should be deactivated."
    assert event3.status == EventStatus.INACTIVE, "Event3 should remain inactive."


def test_deactivate_next_event_last_event_in_queue():
    """Test `deactivate_next_event` when there is only one event in the queue."""
    scheduler = Environment()
    event1 = Event(time=5)

    # Deactivate event1 manually and schedule it
    event1.deactivate()
    scheduler.schedule(event1)

    # Deactivate the next event (event1 is the only event in the queue)
    scheduler.deactivate_next_event()

    # Ensure event1 is deactivated
    assert event1.status == EventStatus.INACTIVE, "Event1 should be deactivated."


def test_deactivate_next_event_after_event_activation():
    """Test `deactivate_next_event` after activating some events."""
    scheduler = Environment()
    event1 = Event(time=5)
    event2 = Event(time=10)
    event3 = Event(time=15)

    # Deactivate all events initially
    event1.deactivate()
    event2.deactivate()
    event3.deactivate()

    # Schedule the events
    scheduler.schedule(event1)
    scheduler.schedule(event2)
    scheduler.schedule(event3)

    # Activate event1
    event1.activate()

    # Deactivate the next event (which should be event1, since it's activated)
    scheduler.deactivate_next_event()

    # Ensure event1 is deactivated
    assert event1.status == EventStatus.INACTIVE, (
        "Event1 should be deactivated after calling deactivate_next_event."
    )


def test_deactivate_next_event_with_unactivated_events():
    """Test `deactivate_next_event` with unactivated events in the queue."""
    scheduler = Environment()
    event1 = Event(time=5)
    event2 = Event(time=10)

    # Deactivate event1 manually and schedule both events
    event1.deactivate()
    event2.deactivate()
    scheduler.schedule(event1)
    scheduler.schedule(event2)

    # Deactivate the next event (event1 should be the first one)
    scheduler.deactivate_next_event()

    # Ensure event1 is deactivated
    assert event1.status == EventStatus.INACTIVE, "Event1 should be deactivated."

    # Ensure event2 remains inactive since it's the next event in the queue
    assert event2.status == EventStatus.INACTIVE, "Event2 should remain inactive."
