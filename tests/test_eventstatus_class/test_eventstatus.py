from desimpy.core import EventStatus


def test_event_status_members():
    """Test that EventStatus contains the correct members."""
    assert hasattr(
        EventStatus, "INACTIVE"
    ), "INACTIVE should be a member of EventStatus."
    assert hasattr(EventStatus, "ACTIVE"), "ACTIVE should be a member of EventStatus."


def test_event_status_values():
    """Test the auto-assigned values of EventStatus members."""
    assert EventStatus.INACTIVE.value == "inactive", "INACTIVE should have a value of 1."
    assert EventStatus.ACTIVE.value == "active", "ACTIVE should have a value of 2."


def test_event_status_comparisons():
    """Test comparisons between EventStatus members."""
    assert (
        EventStatus.INACTIVE != EventStatus.ACTIVE
    ), "INACTIVE and ACTIVE should not be equal."
    assert (
        EventStatus.INACTIVE.value > EventStatus.ACTIVE.value
    ), "INACTIVE should have a smaller value than ACTIVE."


def test_event_status_iteration():
    """Test that EventStatus can be iterated correctly."""
    expected_members = ["INACTIVE", "ACTIVE"]
    actual_members = [status.name for status in EventStatus]
    assert (
        actual_members == expected_members
    ), f"Expected {expected_members}, but got {actual_members}."


def test_event_status_string_representation():
    """Test the string representation of EventStatus members."""
    print(EventStatus.ACTIVE)
    assert (
        str(EventStatus.INACTIVE) == "inactive"
    ), "String representation of INACTIVE is incorrect."
    assert (
        str(EventStatus.ACTIVE) == "active"
    ), "String representation of ACTIVE is incorrect."
