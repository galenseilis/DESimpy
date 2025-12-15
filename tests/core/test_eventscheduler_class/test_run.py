from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Callable

import pytest

from desimpy import Event, Environment


@pytest.fixture
def scheduler() -> Environment:
    """Fixture to create a fresh Environment instance for each test."""
    return Environment()


def test_run_no_events(scheduler: Environment) -> None:
    """Test that run handles an empty event queue gracefully."""
    stop: Callable[[Environment], bool] = lambda sched: True  # Stop immediately
    result = scheduler.run(stop)

    assert scheduler.current_time == 0  # Time should not advance
    assert len(scheduler.event_queue) == 0  # Queue should remain empty
    assert result == []  # No events logged


def test_run_stops_based_on_stop_condition(scheduler: Environment) -> None:
    """Test that run stops when the stop condition is met."""

    def action() -> None:
        pass

    scheduler.schedule(Event(time=5, context={}, action=action))
    scheduler.schedule(Event(time=10, context={}, action=action))

    stop: Callable[[Environment], bool] = (
        lambda sched: sched.current_time >= 5
    )  # Stop after first event
    result = scheduler.run(stop)

    assert scheduler.current_time == 5  # Scheduler stops at the correct time
    assert len(scheduler.event_queue) == 1  # Remaining event is not processed
    assert len(result) == 1  # Only one event was logged


def test_run_processes_all_events(scheduler: Environment) -> None:
    """Test that run processes all events when stop condition allows it."""
    actions_triggered: list[str] = []

    def action_1() -> None:
        actions_triggered.append("event_1")

    def action_2() -> None:
        actions_triggered.append("event_2")

    scheduler.schedule(Event(time=5, context={}, action=action_1))
    scheduler.schedule(Event(time=10, context={}, action=action_2))

    stop: Callable[[Environment], bool] = lambda sched: False  # Never stop
    result: list[Event] = scheduler.run(stop)

    assert scheduler.current_time == 10  # Scheduler processes all events
    assert len(actions_triggered) == 2  # Both actions were executed
    assert len(result) == 2  # Both events were logged
    assert result[0].time == 5
    assert result[1].time == 10


def test_run_logging_disabled(scheduler: Environment) -> None:
    """Test that run does not log events if logging is disabled."""

    def action() -> None:
        pass

    scheduler.schedule(Event(time=5, context={}, action=action))
    scheduler.schedule(Event(time=10, context={}, action=action))

    stop: Callable[[Environment], bool] = lambda sched: False  # Never stop
    result = scheduler.run(stop, logging=False)

    assert scheduler.current_time == 10  # Scheduler processes all events
    assert len(result) == 0  # No events were logged


def test_run_filtered_logging(scheduler: Environment) -> None:
    """Test that run logs only events that pass the logging filter."""

    def action_1() -> None:
        pass

    def action_2() -> None:
        pass

    scheduler.schedule(Event(time=5, context={"type": "important"}, action=action_1))
    scheduler.schedule(Event(time=10, context={"type": "normal"}, action=action_2))

    stop: Callable[[Environment], bool] = lambda sched: False  # Never stop
    log_filter: Callable[[Event], bool] = (
        lambda event: event.context.get("type") == "important"
    )  # Log only "important" events
    result = scheduler.run(stop, logging=log_filter)

    assert scheduler.current_time == 10  # Scheduler processes all events
    assert len(result) == 1  # Only one event was logged
    assert result[0].context["type"] == "important"  # Correct event was logged


def test_run_handles_exceptions(scheduler: Environment) -> None:
    """Test that run propagates exceptions raised by event actions."""

    def faulty_action() -> None:
        raise ValueError("Intentional error")

    scheduler.schedule(Event(time=5, context={}, action=faulty_action))

    stop: Callable[[Environment], bool] = lambda sched: False  # Never stop

    with pytest.raises(ValueError, match="Intentional error"):
        _: list[Event] = scheduler.run(stop)

    assert (
        scheduler.current_time == 5
    )  # Scheduler stops at the time of the faulty event
    assert len(scheduler.event_queue) == 0  # Event queue is cleared


def test_run_stops_midway_due_to_stop_condition(scheduler: Environment) -> None:
    """Test that run stops processing events when the stop condition is met."""
    actions_triggered: list[str] = []

    def action_1() -> None:
        actions_triggered.append("event_1")

    def action_2() -> None:
        actions_triggered.append("event_2")

    scheduler.schedule(Event(time=5, context={}, action=action_1))
    scheduler.schedule(Event(time=10, context={}, action=action_2))

    stop: Callable[[Environment], bool] = (
        lambda sched: sched.current_time >= 5
    )  # Stop after processing the first event
    result = scheduler.run(stop)

    assert scheduler.current_time == 5  # Scheduler stops after the first event
    assert len(actions_triggered) == 1  # Only the first action was executed
    assert len(result) == 1  # Only the first event was logged
    assert len(scheduler.event_queue) == 1  # Second event remains in the queue
