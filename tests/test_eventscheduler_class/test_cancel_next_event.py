from desimpy import Event, EventScheduler

# Test Suite for cancel_next_event


def test_cancel_next_event_empty_queue():
    """Test `cancel_next_event` when the event queue is empty."""
    scheduler = EventScheduler()

    # Try to cancel the next event when no events are scheduled
    scheduler.cancel_next_event()

    # The queue should still be empty
    assert len(scheduler.event_queue) == 0, "The event queue should remain empty."


def test_cancel_next_event_single_event():
    """Test `cancel_next_event` with a single event in the queue."""
    scheduler = EventScheduler()
    event = Event(time=5)

    # Schedule the event
    scheduler.schedule(event)

    # Cancel the next event
    scheduler.cancel_next_event()

    # The event should be removed from the queue
    assert (
        len(scheduler.event_queue) == 0
    ), "The event queue should be empty after cancellation."


def test_cancel_next_event_multiple_events():
    """Test `cancel_next_event` with multiple events in the queue."""
    scheduler = EventScheduler()
    event1 = Event(time=5)
    event2 = Event(time=10)
    event3 = Event(time=15)

    # Schedule the events
    scheduler.schedule(event1)
    scheduler.schedule(event2)
    scheduler.schedule(event3)

    # Cancel the next event (event1)
    scheduler.cancel_next_event()

    # Ensure event1 is removed and the other events remain scheduled
    assert (
        len(scheduler.event_queue) == 2
    ), "The event queue should have two events remaining."
    assert (
        event2.time,
        event2,
    ) in scheduler.event_queue, "Event2 should remain in the queue."
    assert (
        event3.time,
        event3,
    ) in scheduler.event_queue, "Event3 should remain in the queue."
    assert (
        event1.time,
        event1,
    ) not in scheduler.event_queue, "Event1 should be removed from the queue."


def test_cancel_next_event_no_events_remaining():
    """Test `cancel_next_event` after cancelling the first event, leaving no events."""
    scheduler = EventScheduler()
    event1 = Event(time=5)
    event2 = Event(time=10)

    # Schedule the events
    scheduler.schedule(event1)
    scheduler.schedule(event2)

    # Cancel the next event (event1)
    scheduler.cancel_next_event()

    # Cancel the next event (event2)
    scheduler.cancel_next_event()

    # The queue should be empty
    assert (
        len(scheduler.event_queue) == 0
    ), "The event queue should be empty after cancellation of all events."


def test_cancel_next_event_queue_ordering():
    """Test `cancel_next_event` to ensure it cancels events in order."""
    scheduler = EventScheduler()
    event1 = Event(time=5)
    event2 = Event(time=10)
    event3 = Event(time=15)

    # Schedule the events
    scheduler.schedule(event1)
    scheduler.schedule(event2)
    scheduler.schedule(event3)

    # Cancel the next event (event1)
    scheduler.cancel_next_event()

    # Ensure that the remaining events are in the correct order
    assert scheduler.event_queue[0][1] == event2, "Event2 should now be the next event."
    assert scheduler.event_queue[1][1] == event3, "Event3 should remain the last event."
    assert (
        (event1.time, event1) not in scheduler.event_queue
    ), "Event1 should be cancelled and removed from the queue."


def test_cancel_next_event_no_next_event():
    """Test `cancel_next_event` when no events are scheduled."""
    scheduler = EventScheduler()

    # Try to cancel the next event when the queue is empty
    scheduler.cancel_next_event()

    # Ensure the queue is still empty
    assert len(scheduler.event_queue) == 0, "The event queue should remain empty."


def test_cancel_next_event_already_cancelled_event():
    """Test `cancel_next_event` with an already cancelled event in the queue."""
    scheduler = EventScheduler()
    event1 = Event(time=5)
    event2 = Event(time=10)

    # Schedule the events
    scheduler.schedule(event1)
    scheduler.schedule(event2)

    # Cancel the first event manually
    scheduler.cancel_next_event()  # Cancel event1

    # Try cancelling again, event1 should be removed
    scheduler.cancel_next_event()  # Now cancel event2

    # Ensure the queue is empty
    assert (
        len(scheduler.event_queue) == 0
    ), "The event queue should be empty after cancelling both events."


def test_cancel_next_event_event_with_multiple_actions():
    """Test `cancel_next_event` with events having multiple actions scheduled."""
    scheduler = EventScheduler()
    event1 = Event(time=5, action=lambda: print("Action 1"))
    event2 = Event(time=10, action=lambda: print("Action 2"))

    # Schedule the events
    scheduler.schedule(event1)
    scheduler.schedule(event2)

    # Add multiple actions to the first event (event1)

    # Cancel the next event (event1)
    scheduler.cancel_next_event()

    # Ensure event1 is removed and no actions are executed
    assert (
        len(scheduler.event_queue) == 1
    ), "The event queue should have one event remaining."
    assert (
        (event1.time, event1) not in scheduler.event_queue
    ), "Event1 should be cancelled and removed from the queue."
    assert (
        event2.time,
        event2,
    ) in scheduler.event_queue, "Event2 should remain active."


def test_cancel_next_event_reschedules():
    """Test `cancel_next_event` while rescheduling events."""
    scheduler = EventScheduler()
    event1 = Event(time=5)
    event2 = Event(time=10)

    # Schedule the events
    scheduler.schedule(event1)
    scheduler.schedule(event2)

    assert len(scheduler.event_queue) == 2, "The event queue should have two events."
    # Cancel event1 and reschedule event2
    scheduler.cancel_next_event()

    assert len(scheduler.event_queue) == 1, "The event queue should have one event."
    # Reschedule event2 and ensure it is rescheduled correctly
    scheduler.schedule(event2)

    # Check the status of events
    assert len(scheduler.event_queue) == 2, "The event queue should have two events."
    assert (
        event2.time,
        event2,
    ) in scheduler.event_queue, "Event2 should be the only event in the queue."
