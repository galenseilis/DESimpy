from __future__ import annotations

import pytest

from desimpy import Event, Environment


@pytest.fixture
def scheduler() -> Environment:
    """Fixture to create a fresh Environment instance for each test."""
    return Environment()


@pytest.fixture
def sample_events() -> list[Event]:
    """Fixture to provide sample events for testing."""
    return [
        Event(time=5, context={"type": "A"}),
        Event(time=10, context={"type": "B"}),
        Event(time=15, context={"type": "A"}),
        Event(time=20, context={"type": "C"}),
    ]


def test_cancel_all_events_by_condition_removes_matching_events(
    scheduler: Environment,
    sample_events: list[Event],
) -> None:
    """Test that events matching the condition are removed."""
    for event in sample_events:
        scheduler.schedule(event)

    assert len(scheduler.event_queue) == 4

    # Remove events of type 'A'
    scheduler.cancel_all_events_by_condition(
        lambda _, event: event.context.get("type") == "A",
    )
    remaining_events = [event for _, event in scheduler.event_queue]
    assert len(remaining_events) == 2
    assert all(event.context["type"] != "A" for event in remaining_events)


def test_cancel_all_events_by_condition_no_match(
    scheduler: Environment,
    sample_events: list[Event],
) -> None:
    """Test that no events are removed if none match the condition."""
    for event in sample_events:
        scheduler.schedule(event)

    assert len(scheduler.event_queue) == 4

    # Try removing events with a non-existent type
    scheduler.cancel_all_events_by_condition(
        lambda _, event: event.context.get("type") == "D",
    )
    remaining_events = [event for _, event in scheduler.event_queue]
    assert len(remaining_events) == 4


def test_cancel_all_events_by_condition_empty_queue(scheduler: Environment) -> None:
    """Test that the method handles an empty event queue gracefully."""
    assert len(scheduler.event_queue) == 0

    scheduler.cancel_all_events_by_condition(
        lambda _, event: event.context.get("type") == "A",
    )
    assert len(scheduler.event_queue) == 0


def test_cancel_all_events_by_condition_partial_match(
    scheduler: Environment,
    sample_events: list[Event],
) -> None:
    """Test that only events matching the condition are removed."""
    for event in sample_events:
        scheduler.schedule(event)

    assert len(scheduler.event_queue) == 4

    # Remove events where time is less than 15
    scheduler.cancel_all_events_by_condition(lambda _, event: event.time < 15)
    remaining_events = [event for _, event in scheduler.event_queue]
    assert len(remaining_events) == 2
    assert all(event.time >= 15 for event in remaining_events)


def test_cancel_all_events_by_condition_duplicate_context(
    scheduler: Environment,
) -> None:
    """Test that events with duplicate contexts are handled correctly."""
    events = [
        Event(time=5, context={"type": "A"}),
        Event(time=10, context={"type": "A"}),
    ]
    for event in events:
        scheduler.schedule(event)

    assert len(scheduler.event_queue) == 2

    # Remove all events of type 'A'
    scheduler.cancel_all_events_by_condition(
        lambda _, event: event.context.get("type") == "A",
    )
    assert len(scheduler.event_queue) == 0
