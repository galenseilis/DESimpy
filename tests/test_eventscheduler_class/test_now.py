from unittest.mock import Mock

import pytest

from desimpy import Event, EventScheduler


@pytest.fixture
def scheduler():
    return EventScheduler()


def test_now_initial_time(scheduler: EventScheduler) -> None:
    """Test that the initial time is zero."""
    assert scheduler.now == 0, "Initial time should be 0."


def test_now_after_scheduling_events(scheduler: EventScheduler):
    """Test that scheduling events does not alter the current time."""
    mock_event = Mock(spec=Event)
    mock_event.time = 5
    scheduler.schedule(mock_event)
    assert scheduler.now == 0, "Current time should remain 0 after scheduling events."


def test_now_progression_after_step(scheduler: EventScheduler) -> None:
    """Test that current time (`now`) updates correctly as events are processed."""
    # Create and schedule two mock events with different times
    mock_event1 = Mock(spec=Event)
    mock_event1.time = 3
    mock_event2 = Mock(spec=Event)
    mock_event2.time = 7
    scheduler.schedule(mock_event1)
    scheduler.schedule(mock_event2)

    # Step through the first event
    _ = scheduler.step()
    assert scheduler.now == 3, "Current time should update to 3 after the first event."

    # Step through the second event
    _ = scheduler.step()
    assert scheduler.now == 7, "Current time should update to 7 after the second event."


def test_now_stops_at_max_time(scheduler: EventScheduler) -> None:
    """Test that simulation stops at a specified max time."""
    mock_event1 = Mock(spec=Event)
    mock_event1.time = 3
    mock_event2 = Mock(spec=Event)
    mock_event2.time = 7
    scheduler.schedule(mock_event1)
    scheduler.schedule(mock_event2)

    # Run until max time of 5
    _ = scheduler.run_until_max_time(5)
    assert (
        scheduler.now == 5
    ), "Simulation should stop at the first event time before reaching max time 5."

    # Run until max time of 8
    _ = scheduler.run_until_max_time(8)
    assert (
        scheduler.now == 8
    ), "Simulation should stop at the time of the second event before reaching max time 8."
