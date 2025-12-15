import pytest

from desimpy import Event, Environment


@pytest.fixture
def scheduler() -> Environment:
    """Fixture to create a fresh EventScheduler instance for each test."""
    return Environment()


def test_run_until_max_time_no_events(scheduler: Environment) -> None:
    """Test that run_until_max_time handles an empty event queue gracefully."""
    result = scheduler.run_until_max_time(max_time=10)

    assert scheduler.current_time == 10  # Time should not advance
    assert len(scheduler.event_queue) == 0  # Queue should remain empty
    assert result == []  # No events logged


def test_run_until_max_time_all_events_processed(scheduler: Environment) -> None:
    """Test that run_until_max_time processes all events if max_time is sufficient."""
    actions_triggered = []

    def action_1() -> None:
        actions_triggered.append("event_1")

    def action_2() -> None:
        actions_triggered.append("event_2")

    scheduler.schedule(Event(time=5, context={}, action=action_1))
    scheduler.schedule(Event(time=10, context={}, action=action_2))

    result = scheduler.run_until_max_time(max_time=15)

    assert scheduler.current_time == 15  # Scheduler processes all events
    assert len(actions_triggered) == 2  # Both actions were executed
    assert len(result) == 2  # Both events were logged
    assert result[0].time == 5
    assert result[1].time == 10


def test_run_until_max_time_stops_at_max_time(scheduler: Environment) -> None:
    """Test that run_until_max_time stops processing events at max_time."""
    actions_triggered = []

    def action_1() -> None:
        actions_triggered.append("event_1")

    def action_2() -> None:
        actions_triggered.append("event_2")

    scheduler.schedule(Event(time=5, context={}, action=action_1))
    scheduler.schedule(Event(time=10, context={}, action=action_2))

    result = scheduler.run_until_max_time(max_time=7)

    assert scheduler.current_time == 7  # Scheduler stops at max_time
    assert len(actions_triggered) == 1  # Only the first action was executed
    assert len(result) == 1  # Only the first event was logged
    assert result[0].time == 5
    assert len(scheduler.event_queue) == 1  # Second event remains in the queue


def test_run_until_max_time_handles_empty_queue_early_stop(
    scheduler: Environment,
) -> None:
    """Test that run_until_max_time stops if the event queue becomes empty before max_time."""

    def action() -> None:
        pass

    scheduler.schedule(Event(time=5, context={}, action=action))

    result = scheduler.run_until_max_time(max_time=10)

    assert scheduler.current_time == 10  # Scheduler stops at the max time
    assert len(result) == 1  # Only one event was logged
    assert len(scheduler.event_queue) == 0  # Event queue is empty


def test_run_until_max_time_logging_disabled(scheduler: Environment) -> None:
    """Test that run_until_max_time does not log events if logging is disabled."""

    def action() -> None:
        pass

    scheduler.schedule(Event(time=5, context={}, action=action))
    scheduler.schedule(Event(time=10, context={}, action=action))

    result = scheduler.run_until_max_time(max_time=15, logging=False)

    assert scheduler.current_time == 15  # Scheduler processes all events
    assert len(result) == 0  # No events were logged


def test_run_until_max_time_filtered_logging(scheduler: Environment) -> None:
    """Test that run_until_max_time logs only events that pass the logging filter."""

    def action_1() -> None:
        pass

    def action_2() -> None:
        pass

    scheduler.schedule(Event(time=5, context={"type": "important"}, action=action_1))
    scheduler.schedule(Event(time=10, context={"type": "normal"}, action=action_2))

    log_filter = (
        lambda event: event.context.get("type") == "important"
    )  # Log only "important" events
    result = scheduler.run_until_max_time(max_time=15, logging=log_filter)

    assert scheduler.current_time == 15  # Scheduler processes all events
    assert len(result) == 1  # Only one event was logged
    assert result[0].context["type"] == "important"  # Correct event was logged


def test_run_until_max_time_handles_exceptions(scheduler: Environment) -> None:
    """Test that run_until_max_time propagates exceptions raised by event actions."""

    def faulty_action() -> None:
        raise ValueError("Intentional error")

    scheduler.schedule(Event(time=5, context={}, action=faulty_action))

    with pytest.raises(ValueError, match="Intentional error"):
        scheduler.run_until_max_time(max_time=10)

    assert (
        scheduler.current_time == 5
    )  # Scheduler stops at the time of the faulty event
    assert len(scheduler.event_queue) == 0  # Event queue is cleared
