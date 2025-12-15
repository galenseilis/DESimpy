from __future__ import annotations

from collections.abc import Callable

import pytest

from desimpy import Event, Environment


@pytest.fixture
def scheduler() -> Environment:
    """Fixture to create a fresh Environment instance for each test."""
    return Environment()


@pytest.fixture
def event() -> Callable[[float], Event]:
    """Helper function to create an event with a given time."""

    def _create_event(time: float) -> Event:
        return Event(time)

    return _create_event


def test_peek_empty_queue(scheduler: Environment):
    """Test that peek returns infinity when the event queue is empty."""
    assert scheduler.peek() == float("inf")


def test_peek_single_event(scheduler: Environment, event: Callable[[float], Event]):
    """Test that peek returns the time of the only event in the queue."""
    event1 = event(10.0)
    scheduler.schedule(event1)
    assert scheduler.peek() == 10.0


def test_peek_multiple_events_ordered(
    scheduler: Environment,
    event: Callable[[float], Event],
):
    """Test that peek returns the earliest event time with multiple events in chronological order."""
    event1 = event(5.0)
    event2 = event(10.0)
    scheduler.schedule(event1)
    scheduler.schedule(event2)
    assert scheduler.peek() == 5.0


def test_peek_multiple_events_unordered(
    scheduler: Environment,
    event: Callable[[float], Event],
):
    """Test that peek returns the earliest event time even if events are added out of order."""
    event1 = event(10.0)
    event2 = event(3.0)
    event3 = event(7.0)
    scheduler.schedule(event1)
    scheduler.schedule(event2)
    scheduler.schedule(event3)
    assert scheduler.peek() == 3.0


def test_peek_after_event_removal(
    scheduler: Environment,
    event: Callable[[float], Event],
):
    """Test that peek correctly updates after removing the next event."""
    event1 = event(3.0)
    event2 = event(8.0)
    scheduler.schedule(event1)
    scheduler.schedule(event2)

    # Peek should initially return the earliest event time
    assert scheduler.peek() == 3.0

    # Remove the first event and check that peek updates
    scheduler.cancel_next_event()
    assert scheduler.peek() == 8.0


def test_peek_prescheduling_negative_time(
    scheduler: Environment,
    event: Callable[[float], Event],
):
    """Test that peek allows negative event times if prescheduled."""
    event1 = event(-5.0)
    scheduler.schedule(event1)
    assert scheduler.peek() == -5.0


def test_peek_after_all_events_canceled(
    scheduler: Environment,
    event: Callable[[float], Event],
):
    """Test that peek returns infinity after all events are canceled."""
    event1 = event(4.0)
    event2 = event(6.0)
    scheduler.schedule(event1)
    scheduler.schedule(event2)

    # Cancel all events
    scheduler.cancel_all_events()
    assert scheduler.peek() == float("inf")


def test_peek_with_active_status(
    scheduler: Environment,
    event: Callable[[float], Event],
):
    """Test that peek still returns the correct time when the scheduler is active."""
    # WARN: Using private name `_activate`.
    scheduler._activate()
    event1 = event(2.0)
    event2 = event(5.0)
    scheduler.schedule(event1)
    scheduler.schedule(event2)

    assert scheduler.peek() == 2.0
    # WARN: Using private name `_deactivate`.
    scheduler._deactivate()
