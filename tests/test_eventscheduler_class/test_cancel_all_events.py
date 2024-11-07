from desimpy import Event, EventScheduler

# Test Suite for cancel_all_events

def test_cancel_all_events_empty_queue():
    """Test `cancel_all_events` when the event queue is empty."""
    scheduler = EventScheduler()

    # Call cancel_all_events on an empty scheduler
    scheduler.cancel_all_events()

    # The queue should remain empty
    assert len(scheduler.event_queue) == 0, "The event queue should remain empty."

def test_cancel_all_events_single_event():
    """Test `cancel_all_events` when there is only one event in the queue."""
    scheduler = EventScheduler()
    event1 = Event(time=5)

    # Schedule the event
    scheduler.schedule(event1)

    # Call cancel_all_events
    scheduler.cancel_all_events()

    # The queue should be empty
    assert len(scheduler.event_queue) == 0, "The event queue should be empty after canceling all events."
    assert (event1.time, event1) not in scheduler.event_queue, "Event1 should be removed from the queue."

def test_cancel_all_events_multiple_events():
    """Test `cancel_all_events` when there are multiple events in the queue."""
    scheduler = EventScheduler()
    event1 = Event(time=5)
    event2 = Event(time=10)
    event3 = Event(time=15)

    # Schedule the events
    scheduler.schedule(event1)
    scheduler.schedule(event2)
    scheduler.schedule(event3)

    # Call cancel_all_events
    scheduler.cancel_all_events()

    # The queue should be empty
    assert len(scheduler.event_queue) == 0, "The event queue should be empty after canceling all events."
    assert (event1.time, event1) not in scheduler.event_queue, "Event1 should be removed from the queue."
    assert (event2.time, event2) not in scheduler.event_queue, "Event2 should be removed from the queue."
    assert (event3.time, event3) not in scheduler.event_queue, "Event3 should be removed from the queue."

def test_cancel_all_events_with_condition_on_event_attributes():
    """Test `cancel_all_events` when events have different attributes (e.g., time, priority)."""
    scheduler = EventScheduler()
    event1 = Event(time=5, context=dict(priority=1))
    event2 = Event(time=10, context=dict(priority=2))
    event3 = Event(time=15, context=dict(priority=1))

    # Schedule the events
    scheduler.schedule(event1)
    scheduler.schedule(event2)
    scheduler.schedule(event3)

    # Call cancel_all_events
    scheduler.cancel_all_events()

    # The queue should be empty after cancellation
    assert len(scheduler.event_queue) == 0, "The event queue should be empty after canceling all events."
    assert (event1.time, event1) not in scheduler.event_queue, "Event1 should be removed from the queue."
    assert (event2.time, event2) not in scheduler.event_queue, "Event2 should be removed from the queue."
    assert (event3.time, event3) not in scheduler.event_queue, "Event3 should be removed from the queue."

def test_cancel_all_events_with_condition_on_time():
    """Test `cancel_all_events` with events having different times and a time-based condition."""
    scheduler = EventScheduler()
    event1 = Event(time=5)
    event2 = Event(time=10)
    event3 = Event(time=15)

    # Schedule the events
    scheduler.schedule(event1)
    scheduler.schedule(event2)
    scheduler.schedule(event3)

    # Call cancel_all_events with a condition that matches all events
    scheduler.cancel_all_events()

    # The queue should be empty
    assert len(scheduler.event_queue) == 0, "The event queue should be empty after canceling all events."
    assert (event1.time, event1) not in scheduler.event_queue, "Event1 should be removed from the queue."
    assert (event2.time, event2) not in scheduler.event_queue, "Event2 should be removed from the queue."
    assert (event3.time, event3) not in scheduler.event_queue, "Event3 should be removed from the queue."

def test_cancel_all_events_after_some_cancellations():
    """Test `cancel_all_events` after some events have already been canceled."""
    scheduler = EventScheduler()
    event1 = Event(time=5)
    event2 = Event(time=10)
    event3 = Event(time=15)

    # Schedule the events
    scheduler.schedule(event1)
    scheduler.schedule(event2)
    scheduler.schedule(event3)

    # Cancel event1 and event2
    scheduler.cancel_next_event()
    scheduler.cancel_next_event()

    # Now, cancel all remaining events
    scheduler.cancel_all_events()

    # The queue should be empty
    assert len(scheduler.event_queue) == 0, "The event queue should be empty after canceling all events."
    assert (event1.time, event1) not in scheduler.event_queue, "Event1 should be removed from the queue."
    assert (event2.time, event2) not in scheduler.event_queue, "Event2 should be removed from the queue."
    assert (event3.time, event3) not in scheduler.event_queue, "Event3 should be removed from the queue."

def test_cancel_all_events_after_rescheduling():
    """Test `cancel_all_events` after some events have been rescheduled."""
    scheduler = EventScheduler()
    event1 = Event(time=5)
    event2 = Event(time=10)
    event3 = Event(time=15)

    # Schedule the events
    scheduler.schedule(event1)
    scheduler.schedule(event2)
    scheduler.schedule(event3)

    # Reschedule event1 to a new time
    event1.time = 20
    scheduler.schedule(event1)

    # Now, cancel all events
    scheduler.cancel_all_events()

    # The queue should be empty
    assert len(scheduler.event_queue) == 0, "The event queue should be empty after canceling all events."
    assert (event1.time, event1) not in scheduler.event_queue, "Event1 should be removed from the queue."
    assert (event2.time, event2) not in scheduler.event_queue, "Event2 should be removed from the queue."
    assert (event3.time, event3) not in scheduler.event_queue, "Event3 should be removed from the queue."

def test_cancel_all_events_with_edge_case():
    """Test `cancel_all_events` when the event queue has edge cases, such as identical times."""
    scheduler = EventScheduler()
    event1 = Event(time=5)
    event2 = Event(time=5)
    event3 = Event(time=10)

    # Schedule the events
    scheduler.schedule(event1)
    scheduler.schedule(event2)
    scheduler.schedule(event3)

    # Call cancel_all_events
    scheduler.cancel_all_events()

    # The queue should be empty after cancellation
    assert len(scheduler.event_queue) == 0, "The event queue should be empty after canceling all events."
    assert (event1.time, event1) not in scheduler.event_queue, "Event1 should be removed from the queue."
    assert (event2.time, event2) not in scheduler.event_queue, "Event2 should be removed from the queue."
    assert (event3.time, event3) not in scheduler.event_queue, "Event3 should be removed from the queue."

