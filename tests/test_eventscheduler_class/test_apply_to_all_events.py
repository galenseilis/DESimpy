from __future__ import annotations

from collections.abc import Callable

import pytest

from desimpy.core import Event, EventScheduler, EventStatus


@pytest.fixture
def scheduler():
    """Fixture to create a fresh EventScheduler instance for each test."""
    return EventScheduler()


@pytest.fixture
def event() -> Callable[[float], Event]:
    """Helper function to create an event with a given time."""

    def _create_event(time: float) -> Event:
        return Event(time)

    return _create_event


def test_apply_to_all_events_empty_queue(scheduler: EventScheduler):
    """Test that apply_to_all_events does nothing when the event queue is empty."""

    def increment_time(event: Event) -> None:
        event.time += (
            5  # Arbitrary function that would alter event time if events existed
        )

    # No events in the queue, so nothing should change
    scheduler.apply_to_all_events(increment_time)
    assert scheduler.peek() == float("inf")  # Ensure the queue is still empty


def test_apply_to_all_events_increment_time(
    scheduler: EventScheduler, event: Callable[[float], Event]
):
    """Test that apply_to_all_events correctly increments the time of each event."""
    event1 = event(10.0)
    event2 = event(15.0)
    scheduler.schedule(event1)
    scheduler.schedule(event2)

    def increment_time(event: Event) -> None:
        event.time += 5

    scheduler.apply_to_all_events(increment_time)

    # Check that each event's time has been incremented by 5
    assert event1.time == 15.0
    assert event2.time == 20.0
    # Peek should return the new earliest time
    assert scheduler.peek() == 15.0


def test_apply_to_all_events_double_time(
    scheduler: EventScheduler, event: Callable[[float], Event]
):
    """Test that apply_to_all_events doubles the time of each event."""
    event1 = event(2.0)
    event2 = event(4.0)
    scheduler.schedule(event1)
    scheduler.schedule(event2)

    def double_time(event: Event) -> None:
        event.time *= 2

    scheduler.apply_to_all_events(double_time)

    assert event1.time == 4.0
    assert event2.time == 8.0
    assert scheduler.peek() == 4.0


def test_apply_to_all_events_custom_attribute_change(
    scheduler: EventScheduler, event: Callable[[float], Event]
):
    """Test that apply_to_all_events can modify a custom attribute of each event."""
    event1 = event(5.0)
    event2 = event(8.0)
    scheduler.schedule(event1)
    scheduler.schedule(event2)

    # Assume events have an 'active' attribute we want to toggle
    event1.status = EventStatus.ACTIVE
    event2.status = EventStatus.INACTIVE

    def toggle_active(event: Event) -> None:
        event.status = (
            EventStatus.ACTIVE
            if event.status == EventStatus.INACTIVE
            else EventStatus.INACTIVE
        )

    scheduler.apply_to_all_events(toggle_active)

    # Verify the 'active' status was toggled for each event
    assert event1.status == EventStatus.INACTIVE
    assert event2.status == EventStatus.ACTIVE


def test_apply_to_all_events_no_change(
    scheduler: EventScheduler, event: Callable[[float], Event]
):
    """Test that apply_to_all_events makes no changes if the function is a no-op."""
    event1 = event(7.0)
    event2 = event(9.0)
    scheduler.schedule(event1)
    scheduler.schedule(event2)

    def no_op(event: Event) -> None:
        _ = event

    scheduler.apply_to_all_events(no_op)

    # Event times should remain unchanged
    assert event1.time == 7.0
    assert event2.time == 9.0
    assert scheduler.peek() == 7.0


def test_apply_to_all_events_negative_time(
    scheduler: EventScheduler, event: Callable[[float], Event]
):
    """Test that apply_to_all_events allows setting negative times for events."""
    event1 = event(3.0)
    event2 = event(6.0)
    scheduler.schedule(event1)
    scheduler.schedule(event2)

    def set_negative_time(event: Event) -> None:
        event.time = -10.0

    scheduler.apply_to_all_events(set_negative_time)

    # Verify that all events now have the time set to -10.0
    assert event1.time == -10.0
    assert event2.time == -10.0
    assert scheduler.peek() == -10.0
