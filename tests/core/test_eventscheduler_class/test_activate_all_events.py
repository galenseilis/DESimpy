from desimpy.core import Event, Environment, EventStatus


def test_activate_all_events_no_events():
    """Test `activate_all_events` when the event queue is empty."""
    scheduler = Environment()

    scheduler.activate_all_events()  # No events in the queue

    assert scheduler.event_queue == [], (
        "The event queue should remain empty when there are no events to activate."
    )


def test_activate_all_events_single_inactive_event():
    """Test `activate_all_events` with a single inactive event."""
    scheduler = Environment()
    event = Event(time=1)
    event.deactivate()  # Set event as inactive
    scheduler.schedule(event)

    scheduler.activate_all_events()

    assert event.status == EventStatus.ACTIVE, "The single event should be activated."


def test_activate_all_events_multiple_inactive_events():
    """Test `activate_all_events` with multiple inactive events."""
    scheduler = Environment()
    event1 = Event(time=1)
    event2 = Event(time=2)
    event1.deactivate()
    event2.deactivate()

    scheduler.schedule(event1)
    scheduler.schedule(event2)

    scheduler.activate_all_events()

    assert event1.status == EventStatus.ACTIVE, "The first event should be activated."
    assert event2.status == EventStatus.ACTIVE, "The second event should be activated."


def test_activate_all_events_mixed_event_status():
    """Test `activate_all_events` with events of mixed statuses (some active, some inactive)."""
    scheduler = Environment()
    event1 = Event(time=1)
    event2 = Event(time=2)
    event3 = Event(time=3)

    event1.deactivate()
    event2.activate()  # Already active
    event3.deactivate()

    scheduler.schedule(event1)
    scheduler.schedule(event2)
    scheduler.schedule(event3)

    scheduler.activate_all_events()

    assert event1.status == EventStatus.ACTIVE, "The first event should be activated."
    assert event2.status == EventStatus.ACTIVE, "The second event should remain active."
    assert event3.status == EventStatus.ACTIVE, "The third event should be activated."


def test_activate_all_events_all_events_already_active():
    """Test `activate_all_events` when all events are already active."""
    scheduler = Environment()
    event1 = Event(time=1)
    event2 = Event(time=2)

    event1.activate()  # Already active
    event2.activate()  # Already active

    scheduler.schedule(event1)
    scheduler.schedule(event2)

    scheduler.activate_all_events()

    assert event1.status == EventStatus.ACTIVE, "The first event should remain active."
    assert event2.status == EventStatus.ACTIVE, "The second event should remain active."


def test_activate_all_events_with_context_conditions():
    """Test `activate_all_events` with events that have contextual conditions."""
    scheduler = Environment()
    event1 = Event(time=1, context={"priority": "high"})
    event2 = Event(time=2, context={"priority": "low"})
    event3 = Event(time=3, context={"priority": "high"})

    event1.deactivate()
    event2.deactivate()
    event3.deactivate()

    scheduler.schedule(event1)
    scheduler.schedule(event2)
    scheduler.schedule(event3)

    scheduler.activate_all_events()

    assert event1.status == EventStatus.ACTIVE, (
        "The first event with high priority should be activated."
    )
    assert event2.status == EventStatus.ACTIVE, (
        "The low priority event should be activated."
    )
    assert event3.status == EventStatus.ACTIVE, (
        "The second high priority event should be activated."
    )


def test_activate_all_events_with_specific_timing():
    """Test `activate_all_events` when events have specific times and ensure all are activated regardless of time."""
    scheduler = Environment()
    event1 = Event(time=10)
    event2 = Event(time=20)
    event3 = Event(time=30)

    event1.deactivate()
    event2.deactivate()
    event3.deactivate()

    scheduler.schedule(event1)
    scheduler.schedule(event2)
    scheduler.schedule(event3)

    scheduler.activate_all_events()

    assert event1.status == EventStatus.ACTIVE, "Event at time 10 should be activated."
    assert event2.status == EventStatus.ACTIVE, "Event at time 20 should be activated."
    assert event3.status == EventStatus.ACTIVE, "Event at time 30 should be activated."


def test_activate_all_events_with_already_scheduled_and_unscheduled_events():
    """Test `activate_all_events` with events that are scheduled and unscheduled."""
    scheduler = Environment()
    event1 = Event(time=5)
    event2 = Event(time=10)
    event1.deactivate()
    event2.deactivate()

    scheduler.schedule(event1)

    # Only event1 is scheduled, event2 remains unscheduled
    scheduler.activate_all_events()

    assert event1.status == EventStatus.ACTIVE, (
        "The scheduled event should be activated."
    )
    assert event2.status == EventStatus.INACTIVE, (
        "The unscheduled event should remain inactive."
    )


def test_activate_all_events_empty_context():
    """Test `activate_all_events` with an event having an empty context to ensure no interference."""
    scheduler = Environment()
    event = Event(time=1, context={})
    event.deactivate()

    scheduler.schedule(event)

    scheduler.activate_all_events()

    assert event.status == EventStatus.ACTIVE, (
        "Event with empty context should still be activated."
    )


def test_activate_all_events_complex_mixed_events():
    """Complex test with mixed event statuses, times, and context to ensure all inactive events are activated."""
    scheduler = Environment()
    event1 = Event(time=5, context={"type": "A"})
    event2 = Event(time=15, context={"type": "B"})
    event3 = Event(time=25, context={"type": "A"})

    event1.deactivate()
    event2.activate()  # Already active
    event3.deactivate()

    scheduler.schedule(event1)
    scheduler.schedule(event2)
    scheduler.schedule(event3)

    scheduler.activate_all_events()

    assert event1.status == EventStatus.ACTIVE, "Inactive event1 should be activated."
    assert event2.status == EventStatus.ACTIVE, "Active event2 should remain active."
    assert event3.status == EventStatus.ACTIVE, "Inactive event3 should be activated."
