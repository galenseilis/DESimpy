from desimpy.core import Event, EventScheduler, EventStatus


def test_deactivate_all_events_no_events():
    """Test `deactivate_all_events` when the event queue is empty."""
    scheduler = EventScheduler()

    scheduler.deactivate_all_events()  # No events in the queue

    assert (
        scheduler.event_queue == []
    ), "The event queue should remain empty when there are no events to activate."


def test_deactivate_all_events_single_inactive_event():
    """Test `deactivate_all_events` with a single inactive event."""
    scheduler = EventScheduler()
    event = Event(time=1)
    event.deactivate()  # Set event as inactive
    scheduler.schedule(event)

    scheduler.deactivate_all_events()

    assert (
        event.status == EventStatus.INACTIVE
    ), "The single event should be deactivated."


def test_deactivate_all_events_multiple_inactive_events():
    """Test `deactivate_all_events` with multiple inactive events."""
    scheduler = EventScheduler()
    event1 = Event(time=1)
    event2 = Event(time=2)
    event1.deactivate()
    event2.deactivate()

    scheduler.schedule(event1)
    scheduler.schedule(event2)

    scheduler.deactivate_all_events()

    assert (
        event1.status == EventStatus.INACTIVE
    ), "The first event should be deactivated."
    assert (
        event2.status == EventStatus.INACTIVE
    ), "The second event should be deactivated."


def test_deactivate_all_events_mixed_event_status():
    """Test `deactivate_all_events` with events of mixed statuses (some active, some inactive)."""
    scheduler = EventScheduler()
    event1 = Event(time=1)
    event2 = Event(time=2)
    event3 = Event(time=3)

    event1.deactivate()
    event2.activate()  # Already active
    event3.deactivate()

    scheduler.schedule(event1)
    scheduler.schedule(event2)
    scheduler.schedule(event3)

    scheduler.deactivate_all_events()

    assert event1.status == EventStatus.INACTIVE, "The first event should be inactive."
    assert event2.status == EventStatus.INACTIVE, "The second event should be inactive."
    assert event3.status == EventStatus.INACTIVE, "The third event should be inactive."


def test_deactivate_all_events_all_events_already_active():
    """Test `deactivate_all_events` when all events are already active."""
    scheduler = EventScheduler()
    event1 = Event(time=1)
    event2 = Event(time=2)

    event1.activate()  # Already active
    event2.activate()  # Already active

    scheduler.schedule(event1)
    scheduler.schedule(event2)

    scheduler.deactivate_all_events()

    assert event1.status == EventStatus.INACTIVE, "The first event should be inactive."
    assert event2.status == EventStatus.INACTIVE, "The second event should be inactive."


def test_deactivate_all_events_with_context_conditions():
    """Test `deactivate_all_events` with events that have contextual conditions."""
    scheduler = EventScheduler()
    event1 = Event(time=1, context={"priority": "high"})
    event2 = Event(time=2, context={"priority": "low"})
    event3 = Event(time=3, context={"priority": "high"})

    event1.deactivate()
    event2.deactivate()
    event3.deactivate()

    scheduler.schedule(event1)
    scheduler.schedule(event2)
    scheduler.schedule(event3)

    scheduler.deactivate_all_events()

    assert (
        event1.status == EventStatus.INACTIVE
    ), "The first event with high priority should be inactive."
    assert (
        event2.status == EventStatus.INACTIVE
    ), "The low priority event should be inactive."
    assert (
        event3.status == EventStatus.INACTIVE
    ), "The second high priority event should be inactive."


def test_deactivate_all_events_with_specific_timing():
    """Test `deactivate_all_events` when events have specific times and ensure all are activated regardless of time."""
    scheduler = EventScheduler()
    event1 = Event(time=10)
    event2 = Event(time=20)
    event3 = Event(time=30)

    event1.deactivate()
    event2.deactivate()
    event3.deactivate()

    scheduler.schedule(event1)
    scheduler.schedule(event2)
    scheduler.schedule(event3)

    scheduler.deactivate_all_events()

    assert (
        event1.status == EventStatus.INACTIVE
    ), "Event at time 10 should be inactivated."
    assert (
        event2.status == EventStatus.INACTIVE
    ), "Event at time 20 should be inactivated."
    assert (
        event3.status == EventStatus.INACTIVE
    ), "Event at time 30 should be inactivated."


def test_deactivate_all_events_with_already_scheduled_and_unscheduled_events():
    """Test `deactivate_all_events` with events that are scheduled and unscheduled."""
    scheduler = EventScheduler()
    event1 = Event(time=5)
    event2 = Event(time=10)
    event1.deactivate()
    event2.deactivate()

    scheduler.schedule(event1)

    # Only event1 is scheduled, event2 remains unscheduled
    scheduler.deactivate_all_events()

    assert (
        event1.status == EventStatus.INACTIVE
    ), "The scheduled event should be inactive."
    assert (
        event2.status == EventStatus.INACTIVE
    ), "The unscheduled event should be inactive."


def test_deactivate_all_events_empty_context():
    """Test `deactivate_all_events` with an event having an empty context to ensure no interference."""
    scheduler = EventScheduler()
    event = Event(time=1, context={})
    event.deactivate()

    scheduler.schedule(event)

    scheduler.deactivate_all_events()

    assert (
        event.status == EventStatus.INACTIVE
    ), "Event with empty context should be inactive."


def test_deactivate_all_events_complex_mixed_events():
    """Complex test with mixed event statuses, times, and context to ensure all inactive events are activated."""
    scheduler = EventScheduler()
    event1 = Event(time=5, context={"type": "A"})
    event2 = Event(time=15, context={"type": "B"})
    event3 = Event(time=25, context={"type": "A"})

    event1.deactivate()
    event2.activate()  # Already active
    event3.deactivate()

    scheduler.schedule(event1)
    scheduler.schedule(event2)
    scheduler.schedule(event3)

    scheduler.deactivate_all_events()

    assert event1.status == EventStatus.INACTIVE, "Inactive event1 should be inactive."
    assert (
        event2.status == EventStatus.INACTIVE
    ), "Active event2 should remain inactive."
    assert event3.status == EventStatus.INACTIVE, "Inactive event3 should be inactive."
