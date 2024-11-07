from desimpy import Event, EventScheduler, EventStatus


def test_activate_next_event_by_condition_single_event_true():
    """Test `activate_next_event_by_condition` with a single event that meets the condition."""
    scheduler = EventScheduler()
    event = Event(time=1)
    event.deactivate()
    scheduler.schedule(event)

    scheduler.activate_next_event_by_condition(lambda s, e: e.time == 1)

    assert (
        event.status == EventStatus.ACTIVE
    ), "The event should be activated as it meets the condition."


def test_activate_next_event_by_condition_single_event_false():
    """Test `activate_next_event_by_condition` with a single event that does not meet the condition."""
    scheduler = EventScheduler()
    event = Event(time=1)
    event.deactivate()
    scheduler.schedule(event)

    scheduler.activate_next_event_by_condition(lambda s, e: e.time == 2)

    assert (
        event.status == EventStatus.INACTIVE
    ), "The event should remain inactive as it does not meet the condition."


def test_activate_next_event_by_condition_multiple_events_first_meets_condition():
    """Test `activate_next_event_by_condition` with multiple events where only the first event meets the condition."""
    scheduler = EventScheduler()
    event1 = Event(time=1)
    event2 = Event(time=2)
    event1.deactivate()
    event2.deactivate()

    scheduler.schedule(event1)
    scheduler.schedule(event2)

    scheduler.activate_next_event_by_condition(lambda s, e: e.time == 1)

    assert (
        event1.status == EventStatus.ACTIVE
    ), "The first event should be activated as it meets the condition."
    assert (
        event2.status == EventStatus.INACTIVE
    ), "The second event should remain inactive as it does not meet the condition."


def test_activate_next_event_by_condition_multiple_events_second_meets_condition():
    """Test `activate_next_event_by_condition` with multiple events where only the second event meets the condition."""
    scheduler = EventScheduler()
    event1 = Event(time=1)
    event2 = Event(time=2)
    event1.deactivate()
    event2.deactivate()

    scheduler.schedule(event1)
    scheduler.schedule(event2)

    scheduler.activate_next_event_by_condition(lambda s, e: e.time == 2)

    assert (
        event1.status == EventStatus.INACTIVE
    ), "The first event should remain inactive as it does not meet the condition."
    assert (
        event2.status == EventStatus.ACTIVE
    ), "The second event should be activated as it meets the condition."


def test_activate_next_event_by_condition_no_events_meet_condition():
    """Test `activate_next_event_by_condition` with multiple events where none meet the condition."""
    scheduler = EventScheduler()
    event1 = Event(time=1)
    event2 = Event(time=2)
    event1.deactivate()
    event2.deactivate()

    scheduler.schedule(event1)
    scheduler.schedule(event2)

    scheduler.activate_next_event_by_condition(lambda s, e: e.time == 3)

    assert (
        event1.status == EventStatus.INACTIVE
    ), "The first event should remain inactive as it does not meet the condition."
    assert (
        event2.status == EventStatus.INACTIVE
    ), "The second event should remain inactive as it does not meet the condition."


def test_activate_next_event_by_condition_first_match_only():
    """Ensure `activate_next_event_by_condition` only activates the first event that meets the condition."""
    scheduler = EventScheduler()
    event1 = Event(time=1)
    event2 = Event(time=1)  # Same time, but only one should be activated
    event1.deactivate()
    event2.deactivate()

    scheduler.schedule(event1)
    scheduler.schedule(event2)

    scheduler.activate_next_event_by_condition(lambda s, e: e.time == 1)

    assert (
        event1.status == EventStatus.ACTIVE
    ), "The first event matching the condition should be activated."
    assert (
        event2.status == EventStatus.INACTIVE
    ), "The second event with the same time should remain inactive."


def test_activate_next_event_by_condition_empty_queue():
    """Test `activate_next_event_by_condition` when the event queue is empty."""
    scheduler = EventScheduler()

    scheduler.activate_next_event_by_condition(
        lambda s, e: e.time == 1
    )  # No events in the queue

    assert (
        scheduler.event_queue == []
    ), "Queue should remain empty when no events are scheduled."


def test_activate_next_event_by_condition_multiple_conditions():
    """Test `activate_next_event_by_condition` with multiple conditions in lambda."""
    scheduler = EventScheduler()
    event1 = Event(time=1, context={"type": "A"})
    event2 = Event(time=2, context={"type": "B"})
    event3 = Event(time=3, context={"type": "A"})
    event1.deactivate()
    event2.deactivate()
    event3.deactivate()

    scheduler.schedule(event1)
    scheduler.schedule(event2)
    scheduler.schedule(event3)

    scheduler.activate_next_event_by_condition(
        lambda s, e: e.context.get("type") == "A" and e.time == 3
    )

    assert (
        event1.status == EventStatus.INACTIVE
    ), "The first event should remain inactive as it does not meet all conditions."
    assert (
        event2.status == EventStatus.INACTIVE
    ), "The second event should remain inactive as it does not meet the conditions."
    assert (
        event3.status == EventStatus.ACTIVE
    ), "The third event should be activated as it meets all conditions."


def test_activate_next_event_by_condition_with_no_match_in_complex_condition():
    """Test `activate_next_event_by_condition` with a complex condition where no event matches."""
    scheduler = EventScheduler()
    event1 = Event(time=1, context={"type": "A"})
    event2 = Event(time=2, context={"type": "B"})
    event1.deactivate()
    event2.deactivate()

    scheduler.schedule(event1)
    scheduler.schedule(event2)

    scheduler.activate_next_event_by_condition(
        lambda s, e: e.context.get("type") == "C"
    )

    assert (
        event1.status == EventStatus.INACTIVE
    ), "The first event should remain inactive as it does not meet the condition."
    assert (
        event2.status == EventStatus.INACTIVE
    ), "The second event should remain inactive as it does not meet the condition."
