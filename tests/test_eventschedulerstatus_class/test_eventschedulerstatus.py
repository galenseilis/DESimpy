from desimpy.core import EventSchedulerStatus

def test_event_scheduler_status_auto_values():
    """Verify the auto-assigned values for the EventSchedulerStatus enum."""
    assert (
        EventSchedulerStatus.INACTIVE.value == "inactive"
    ), "INACTIVE should have a value of inactive."
    assert EventSchedulerStatus.ACTIVE.value == "active", "ACTIVE should have a value of active."


def test_event_scheduler_status_distinction():
    """Ensure that EventSchedulerStatus members are distinct."""
    assert (
        EventSchedulerStatus.INACTIVE != EventSchedulerStatus.ACTIVE
    ), "INACTIVE and ACTIVE should be distinct."


def test_event_scheduler_status_iteration():
    """Verify that all members of EventSchedulerStatus can be iterated over correctly."""
    expected_values = [EventSchedulerStatus.INACTIVE, EventSchedulerStatus.ACTIVE]
    actual_values = list(EventSchedulerStatus)
    assert (
        actual_values == expected_values
    ), f"Expected {expected_values}, got {actual_values}."


def test_event_scheduler_status_names():
    """Verify the names of the EventSchedulerStatus members."""
    assert (
        EventSchedulerStatus.INACTIVE.name == "INACTIVE"
    ), "The name of INACTIVE should be 'INACTIVE'."
    assert (
        EventSchedulerStatus.ACTIVE.name == "ACTIVE"
    ), "The name of ACTIVE should be 'ACTIVE'."


def test_event_scheduler_status_str_representation():
    """Ensure the string representation of EventSchedulerStatus members is correct."""
    assert (
        str(EventSchedulerStatus.INACTIVE) == "inactive"
    ), "String representation of INACTIVE is incorrect."
    assert (
        str(EventSchedulerStatus.ACTIVE) == "active"
    ), "String representation of ACTIVE is incorrect."
