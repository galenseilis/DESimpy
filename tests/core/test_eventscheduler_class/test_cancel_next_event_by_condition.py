from desimpy import Event, Environment

# Test Suite for cancel_next_event_by_condition


def test_cancel_next_event_by_condition_empty_queue():
    """Test `cancel_next_event_by_condition` when the event queue is empty."""
    scheduler = Environment()

    # Condition to cancel events
    def condition(scheduler: Environment, event: Event):
        _ = scheduler
        return event.time == 5

    # Try to cancel the next event with the condition
    scheduler.cancel_next_event_by_condition(condition)

    # The queue should remain empty
    assert len(scheduler.event_queue) == 0, "The event queue should remain empty."


def test_cancel_next_event_by_condition_no_matching_event():
    """Test `cancel_next_event_by_condition` when no event satisfies the condition."""
    scheduler = Environment()
    event1 = Event(time=5)
    event2 = Event(time=10)

    # Schedule the events
    scheduler.schedule(event1)
    scheduler.schedule(event2)

    # Condition to cancel event with time 15, which does not exist
    def condition(scheduler: Environment, event: Event):
        _ = scheduler
        return event.time == 15

    # Try to cancel the next event with the condition
    scheduler.cancel_next_event_by_condition(condition)

    # The event queue should remain unchanged
    assert len(scheduler.event_queue) == 2, "The event queue should have two events."
    assert (
        event1.time,
        event1,
    ) in scheduler.event_queue, "Event1 should remain in the queue."
    assert (
        event2.time,
        event2,
    ) in scheduler.event_queue, "Event2 should remain in the queue."


def test_cancel_next_event_by_condition_single_matching_event():
    """Test `cancel_next_event_by_condition` when one event matches the condition."""
    scheduler = Environment()
    event1 = Event(time=5)
    event2 = Event(time=10)

    # Schedule the events
    scheduler.schedule(event1)
    scheduler.schedule(event2)

    # Condition to cancel event with time 5
    def condition(scheduler: Environment, event: Event):
        _ = scheduler
        return event.time == 5

    # Cancel the next event that matches the condition
    scheduler.cancel_next_event_by_condition(condition)

    # Ensure event1 is removed and event2 remains
    assert len(scheduler.event_queue) == 1, (
        "The event queue should have one event remaining."
    )
    assert (
        event2.time,
        event2,
    ) in scheduler.event_queue, "Event2 should remain in the queue."
    assert (
        event1.time,
        event1,
    ) not in scheduler.event_queue, "Event1 should be removed from the queue."


def test_cancel_next_event_by_condition_multiple_matching_events():
    """Test `cancel_next_event_by_condition` with multiple events matching the condition."""
    scheduler = Environment()
    event1 = Event(time=5)
    event2 = Event(time=5)
    event3 = Event(time=10)

    # Schedule the events
    scheduler.schedule(event1)
    scheduler.schedule(event2)
    scheduler.schedule(event3)

    # Condition to cancel event with time 5
    def condition(scheduler: Environment, event: Event):
        _ = scheduler
        return event.time == 5

    # Cancel the next event that matches the condition
    scheduler.cancel_next_event_by_condition(condition)

    # Ensure one of the events with time 5 is removed and the others remain
    assert len(scheduler.event_queue) == 2, (
        "The event queue should have two events remaining."
    )
    assert (
        event3.time,
        event3,
    ) in scheduler.event_queue, "Event3 should remain in the queue."
    assert (
        (event1.time, event1) not in scheduler.event_queue
        and (event2.time, event2) in scheduler.event_queue
    ) or (
        (event1.time, event1) in scheduler.event_queue
        and (event2.time, event2) not in scheduler.event_queue
    ), "One of the events with time 5 should be removed."


def test_cancel_next_event_by_condition_multiple_events_different_times():
    """Test `cancel_next_event_by_condition` where events have different times."""
    scheduler = Environment()
    event1 = Event(time=5)
    event2 = Event(time=10)
    event3 = Event(time=15)

    # Schedule the events
    scheduler.schedule(event1)
    scheduler.schedule(event2)
    scheduler.schedule(event3)

    # Condition to cancel event with time 10
    def condition(scheduler: Environment, event: Event):
        _ = scheduler
        return event.time == 10

    # Cancel the next event that matches the condition
    scheduler.cancel_next_event_by_condition(condition)

    # Ensure event2 is removed and event1 and event3 remain
    assert len(scheduler.event_queue) == 2, (
        "The event queue should have two events remaining."
    )
    assert (
        event1.time,
        event1,
    ) in scheduler.event_queue, "Event1 should remain in the queue."
    assert (
        event3.time,
        event3,
    ) in scheduler.event_queue, "Event3 should remain in the queue."
    assert (
        event2.time,
        event2,
    ) not in scheduler.event_queue, "Event2 should be removed from the queue."


def test_cancel_next_event_by_condition_condition_with_multiple_parameters():
    """Test `cancel_next_event_by_condition` with a more complex condition."""
    scheduler = Environment()
    event1 = Event(time=5, context=dict(priority=1))
    event2 = Event(time=10, context=dict(priority=2))

    # Schedule the events
    scheduler.schedule(event1)
    scheduler.schedule(event2)

    # Condition to cancel event with priority 2
    def condition(scheduler: Environment, event: Event):
        _ = scheduler
        result: bool = event.context.get("priority") == 2
        return result

    # Cancel the next event that matches the condition
    scheduler.cancel_next_event_by_condition(condition)

    # Ensure event2 is removed and event1 remains
    assert len(scheduler.event_queue) == 1, (
        "The event queue should have one event remaining."
    )
    assert (
        event1.time,
        event1,
    ) in scheduler.event_queue, "Event1 should remain in the queue."
    assert (
        event2.time,
        event2,
    ) not in scheduler.event_queue, "Event2 should be removed from the queue."


def test_cancel_next_event_by_condition_no_matching_condition():
    """Test `cancel_next_event_by_condition` where no event matches the condition."""
    scheduler = Environment()
    event1 = Event(time=5)
    event2 = Event(time=10)

    # Schedule the events
    scheduler.schedule(event1)
    scheduler.schedule(event2)

    # Condition to cancel event with time 20, which does not exist
    def condition(scheduler: Environment, event: Event):
        _ = scheduler
        return event.time == 20

    # Try to cancel the next event with the condition
    scheduler.cancel_next_event_by_condition(condition)

    # The event queue should remain unchanged
    assert len(scheduler.event_queue) == 2, "The event queue should have two events."
    assert (
        event1.time,
        event1,
    ) in scheduler.event_queue, "Event1 should remain in the queue."
    assert (
        event2.time,
        event2,
    ) in scheduler.event_queue, "Event2 should remain in the queue."


def test_cancel_next_event_by_condition_with_condition_having_edge_case():
    """Test `cancel_next_event_by_condition` with an edge case (e.g., cancelling at exact time)."""
    scheduler = Environment()
    event1 = Event(time=5)
    event2 = Event(time=10)

    # Schedule the events
    scheduler.schedule(event1)
    scheduler.schedule(event2)

    # Edge case: Condition to cancel the event at time 5
    def condition(scheduler: Environment, event: Event):
        _ = scheduler
        return event.time == 5

    # Cancel the next event that matches the condition
    scheduler.cancel_next_event_by_condition(condition)

    # Ensure event1 is removed and event2 remains
    assert len(scheduler.event_queue) == 1, (
        "The event queue should have one event remaining."
    )
    assert (
        event2.time,
        event2,
    ) in scheduler.event_queue, "Event2 should remain in the queue."
    assert (
        event1.time,
        event1,
    ) not in scheduler.event_queue, "Event1 should be removed from the queue."
