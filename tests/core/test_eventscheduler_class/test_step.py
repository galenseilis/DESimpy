from __future__ import annotations

import pytest

from desimpy import Event, Environment


@pytest.fixture
def scheduler() -> Environment:
    """Fixture to create a fresh EventScheduler instance for each test."""
    return Environment()


def test_step_processes_one_event(scheduler: Environment) -> None:
    """Test that step processes the next event and removes it from the queue."""
    processed_events: list[int] = []

    # Schedule an event with an action
    scheduler.schedule(
        Event(time=5, context={"id": 1}, action=lambda: processed_events.append(1)),
    )
    scheduler.schedule(Event(time=10, context={"id": 2}))

    # Ensure the queue has two events
    assert len(scheduler.event_queue) == 2

    # Perform one step
    _: Event = scheduler.step()

    # Check that the first event was processed
    assert scheduler.current_time == 5
    assert len(scheduler.event_queue) == 1
    assert processed_events == [1]


def test_step_advances_time_correctly(scheduler: Environment) -> None:
    """Test that step advances the simulation time to the next event."""
    scheduler.schedule(Event(time=15, context={"id": 1}))
    scheduler.schedule(Event(time=10, context={"id": 2}))

    # Perform one step
    _: Event = scheduler.step()

    # Time should advance to 10 (time of first event in priority order)
    assert scheduler.current_time == 10
    assert len(scheduler.event_queue) == 1


def test_step_empty_queue(scheduler: Environment) -> None:
    """Test that step does nothing when the queue is empty."""
    # Ensure queue is empty
    assert len(scheduler.event_queue) == 0
    assert scheduler.current_time == 0

    # Perform a step
    with pytest.raises(IndexError, match="index out of range"):
        _: Event = scheduler.step()

    # Current time should remain the same
    assert scheduler.current_time == 0
    assert len(scheduler.event_queue) == 0


def test_step_executes_event_action(scheduler: Environment) -> None:
    """Test that step executes the action associated with the next event."""
    result: list[str] = []

    def example_action() -> None:
        result.append("executed")

    scheduler.schedule(Event(time=5, context={}, action=example_action))

    # Perform one step
    _: Event = scheduler.step()

    # Ensure the action was executed
    assert result == ["executed"]


def test_step_with_multiple_events(scheduler: Environment) -> None:
    """Test that step processes events in the correct time order."""
    result: list[int] = []

    scheduler.schedule(
        Event(time=20, context={"id": 1}, action=lambda: result.append(1)),
    )
    scheduler.schedule(
        Event(time=10, context={"id": 2}, action=lambda: result.append(2)),
    )
    scheduler.schedule(
        Event(time=15, context={"id": 3}, action=lambda: result.append(3)),
    )

    # Perform multiple steps
    _: Event = scheduler.step()  # Should process event with time=10
    assert scheduler.current_time == 10
    assert result == [2]

    _: Event = scheduler.step()  # Should process event with time=15
    assert scheduler.current_time == 15
    assert result == [2, 3]

    _: Event = scheduler.step()  # Should process event with time=20
    assert scheduler.current_time == 20
    assert result == [2, 3, 1]


def test_step_handles_action_exceptions(scheduler: Environment) -> None:
    """Test that step propagates exceptions raised by event actions."""

    def faulty_action() -> None:
        raise ValueError("Intentional error")

    scheduler.schedule(Event(time=5, context={}, action=faulty_action))

    # Perform one step; exception should propagate
    with pytest.raises(ValueError, match="Intentional error"):
        _: Event = scheduler.step()

    # The current time and event queue should remain unchanged
    assert scheduler.current_time == 5
    assert len(scheduler.event_queue) == 0


def test_step_multiple_steps(scheduler: Environment):
    """Test that multiple steps correctly process all events."""
    result: list[int] = []

    scheduler.schedule(
        Event(time=5, context={"id": 1}, action=lambda: result.append(1)),
    )
    scheduler.schedule(
        Event(time=15, context={"id": 2}, action=lambda: result.append(2)),
    )
    scheduler.schedule(
        Event(time=10, context={"id": 3}, action=lambda: result.append(3)),
    )

    # Perform all steps
    while scheduler.event_queue:
        _: Event = scheduler.step()

    # Check that events were processed in order
    assert scheduler.current_time == 15
    assert result == [1, 3, 2]
