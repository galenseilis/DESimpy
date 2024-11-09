from typing import Any
from collections.abc import Callable

import pytest

from desimpy import Event, EventScheduler, EventStatus


@pytest.fixture
def scheduler() -> EventScheduler:
    """Fixture to create a fresh EventScheduler instance for each test."""
    return EventScheduler()


@pytest.fixture
def event() -> Callable[[float], Event]:
    """Helper function to create an event with a given time."""

    def _create_event(time: float) -> Event:
        return Event(time)

    return _create_event


def test_apply_to_events_by_condition_no_matching_events(
    scheduler: EventScheduler, event: Callable[[float], Event]
) -> None:
    """Test that apply_to_events_by_condition does nothing when no events match the condition."""
    event1 = event(10.0)
    event2 = event(15.0)
    scheduler.schedule(event1)
    scheduler.schedule(event2)

    def condition(s: EventScheduler, e: Event) -> bool:
        _ = s
        return e.time > 20.0  # No event should match this condition

    def increment_time(e: Event) -> Any:
        e.time += 5  # Arbitrary function to alter time

    scheduler.apply_to_events_by_condition(increment_time, condition)

    # Verify that no event times have been modified
    assert event1.time == 10.0
    assert event2.time == 15.0


def test_apply_to_events_by_condition_matching_events(
    scheduler: EventScheduler, event: Callable[[float], Event]
) -> None:
    """Test that apply_to_events_by_condition modifies only the events that match the condition."""
    event1 = event(5.0)
    event2 = event(15.0)
    event3 = event(25.0)
    scheduler.schedule(event1)
    scheduler.schedule(event2)
    scheduler.schedule(event3)

    def condition(s: EventScheduler, e: Event) -> bool:
        _ = s
        return e.time > 10.0  # Only event2 and event3 should match

    def increment_time(e: Event) -> None:
        e.time += 5

    scheduler.apply_to_events_by_condition(increment_time, condition)

    # Check that only event2 and event3 were modified
    assert event1.time == 5.0
    assert event2.time == 20.0
    assert event3.time == 30.0


def test_apply_to_events_by_condition_toggle_attribute(
    scheduler: EventScheduler, event: Callable[[float], Event]
) -> None:
    """Test that apply_to_events_by_condition can toggle an attribute based on a condition."""
    event1 = event(5.0)
    event2 = event(15.0)
    scheduler.schedule(event1)
    scheduler.schedule(event2)

    # Assume events have an 'active' attribute that we want to toggle
    event1.status = EventStatus.ACTIVE
    event2.status = EventStatus.INACTIVE

    def condition(s: EventScheduler, e: Event) -> bool:
        _ = s
        return e.time >= 10.0  # Only event2 should match

    def toggle_active(e: Event) -> None:
        e.status = (
            EventStatus.ACTIVE
            if e.status == EventStatus.INACTIVE
            else EventStatus.ACTIVE
        )

    scheduler.apply_to_events_by_condition(toggle_active, condition)

    # Verify that the 'active' status was toggled only for event2
    event1.status = EventStatus.ACTIVE
    event2.status = EventStatus.ACTIVE


def test_apply_to_events_by_condition_reset_time(
    scheduler: EventScheduler, event: Callable[[float], Event]
) -> None:
    """Test that apply_to_events_by_condition can reset the time of matched events."""
    event1 = event(3.0)
    event2 = event(6.0)
    event3 = event(9.0)
    scheduler.schedule(event1)
    scheduler.schedule(event2)
    scheduler.schedule(event3)

    def condition(s: EventScheduler, e: Event) -> bool:
        _ = s
        return e.time < 7.0  # Only event1 and event2 should match

    def reset_time(e: Event) -> None:
        e.time = 0.0

    scheduler.apply_to_events_by_condition(reset_time, condition)

    # Verify that times were reset only for events that matched the condition
    assert event1.time == 0.0
    assert event2.time == 0.0
    assert event3.time == 9.0


def test_apply_to_events_by_condition_no_op(
    scheduler: EventScheduler, event: Callable[[float], Event]
) -> None:
    """Test that apply_to_events_by_condition makes no changes if the function is a no-op."""
    event1 = event(7.0)
    event2 = event(9.0)
    scheduler.schedule(event1)
    scheduler.schedule(event2)

    def condition(s: EventScheduler, e: Event) -> bool:
        _ = s
        return e.time > 5.0  # Both events should match

    def no_op(e: Event) -> None:
        _ = e  # Function does nothing

    scheduler.apply_to_events_by_condition(no_op, condition)

    # Event times should remain unchanged
    assert event1.time == 7.0
    assert event2.time == 9.0


def test_apply_to_events_by_condition_negative_time(
    scheduler: EventScheduler, event: Callable[[float], Event]
) -> None:
    """Test that apply_to_events_by_condition allows setting negative times for matched events."""
    event1 = event(5.0)
    event2 = event(10.0)
    scheduler.schedule(event1)
    scheduler.schedule(event2)

    def condition(s: EventScheduler, e: Event) -> bool:
        _ = s
        return e.time >= 5.0  # Both events should match

    def set_negative_time(e: Event) -> None:
        e.time = -10.0

    scheduler.apply_to_events_by_condition(set_negative_time, condition)

    # Verify that both events now have the time set to -10.0
    assert event1.time == -10.0
    assert event2.time == -10.0
