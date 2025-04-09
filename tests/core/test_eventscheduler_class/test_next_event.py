from desimpy import Event, EventScheduler


def test_empty_event_queue():
    """Should return None if event queue is empty."""
    env = EventScheduler()
    result = env.next_event()
    assert result is None


def test_preserves_event_identity():
    """Should not change the event."""
    env = EventScheduler()
    event = Event(0, lambda: None, None)
    env.schedule(event)
    result = env.next_event()
    assert result == event


def test_is_next_among_other_events():
    """Should actually be the next event even among other events."""
    env = EventScheduler()

    # Define events occuring at different time.
    last_event = Event(3)
    second_event = Event(2)
    first_event = Event(1)

    # Schedule events in haphazard order.
    env.schedule(second_event)
    env.schedule(first_event)
    env.schedule(last_event)

    # Get next event
    result = env.next_event()

    # Check if next event is the earliest in time.
    assert result == first_event


def test_is_next_after_elapsed_time():
    """Next event evolves with simulation."""
    env = EventScheduler()

    # Define events occuring at different time.
    last_event = Event(3)
    second_event = Event(2)
    first_event = Event(1)

    # Schedule events in haphazard order.
    env.schedule(second_event)
    env.schedule(first_event)
    env.schedule(last_event)

    env.run_until_max_time(1.5)

    # Get next event
    result = env.next_event()

    # Check if next event is the second
    # since the first event should have
    # elapsed.
    assert result == second_event
