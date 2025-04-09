from __future__ import annotations

from collections.abc import Callable
from typing import Any

import pytest

from desimpy.core import Event, EventScheduler, EventStatus


@pytest.fixture
def scheduler() -> EventScheduler:
    """Fixture to create a fresh EventScheduler instance for each test."""
    return EventScheduler()


@pytest.fixture
def event_factory() -> Callable[
    [float, Callable[[], Any], dict[Any, Any] | None], Event,
]:
    """Factory fixture to create events at a specified time with an optional action."""

    def _create_event(
        time: float,
        action: Callable[[], Any] | None = None,
        context: dict[Any, Any] | None = None,
    ):
        return Event(time=time, action=action, context=context)

    return _create_event


EVENT_FACTORY_TYPE = Callable[
    [], Callable[[float, Callable[[], Any], dict[Any, Any] | None], Event],
]


def test_activate_next_event_single_event(scheduler: EventScheduler):
    """Test `activate_next_event` with a single inactive event in the queue."""
    event = Event(1)
    event.deactivate()
    scheduler.schedule(event)

    scheduler.activate_next_event()

    assert event.status == EventStatus.ACTIVE, "The single event should be activated."


def test_activate_next_event_multiple_events(scheduler: EventScheduler):
    """Test `activate_next_event` activates only the earliest event in a queue of multiple events."""
    event1 = Event(time=1)
    event2 = Event(time=2)
    event1.deactivate()
    event2.deactivate()

    scheduler.schedule(event2)  # Later event
    scheduler.schedule(event1)  # Earliest event

    scheduler.activate_next_event()

    assert event1.status == EventStatus.ACTIVE, (
        "The earliest event should be activated."
    )
    assert event2.status == EventStatus.INACTIVE, (
        "The later event should remain inactive."
    )


def test_activate_next_event_with_active_event(scheduler: EventScheduler):
    """Test `activate_next_event` does not change the status of an already active event."""
    event = Event(time=1)
    scheduler.schedule(event)

    scheduler.activate_next_event()  # First activation call
    scheduler.activate_next_event()  # Second activation should have no effect

    assert event.status == EventStatus.ACTIVE, (
        "Event should remain active after reactivation."
    )


def test_activate_next_event_empty_queue(scheduler: EventScheduler):
    """Test `activate_next_event` with an empty event queue."""
    scheduler.activate_next_event()  # Should have no effect, no exception should occur
    assert scheduler.event_queue == [], (
        "Queue should remain empty when no events are scheduled."
    )


def test_activate_next_event_does_not_alter_later_events(scheduler: EventScheduler):
    """Ensure that `activate_next_event` activates only the next event and does not modify later events."""
    event1 = Event(time=1)
    event2 = Event(time=2)
    event1.deactivate()
    event2.deactivate()

    scheduler.schedule(event1)
    scheduler.schedule(event2)

    scheduler.activate_next_event()

    assert event1.status == EventStatus.ACTIVE, "The first event should be activated."
    assert event2.status == EventStatus.INACTIVE, (
        "The second event should remain inactive."
    )


def test_activate_next_event_only_affects_next(scheduler: EventScheduler):
    """Ensure that calling `activate_next_event` only activates one event even if multiple are inactive."""
    event1 = Event(time=1)
    event2 = Event(time=1.5)
    event1.deactivate()
    event2.deactivate()

    scheduler.schedule(event1)
    scheduler.schedule(event2)

    scheduler.activate_next_event()

    assert event1.status == EventStatus.ACTIVE, (
        "Only the earliest event should be activated."
    )
    assert event2.status == EventStatus.INACTIVE, (
        "Subsequent events should remain inactive."
    )
