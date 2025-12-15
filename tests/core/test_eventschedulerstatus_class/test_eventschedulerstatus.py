from desimpy.core import EnvironmentStatus


def test_event_scheduler_status_auto_values():
    """Verify the auto-assigned values for the EnvironmentStatus enum."""
    assert EnvironmentStatus.INACTIVE.value == "inactive", (
        "INACTIVE should have a value of inactive."
    )
    assert EnvironmentStatus.ACTIVE.value == "active", (
        "ACTIVE should have a value of active."
    )


def test_event_scheduler_status_distinction():
    """Ensure that EnvironmentStatus members are distinct."""
    assert EnvironmentStatus.INACTIVE != EnvironmentStatus.ACTIVE, (
        "INACTIVE and ACTIVE should be distinct."
    )


def test_event_scheduler_status_iteration():
    """Verify that all members of EnvironmentStatus can be iterated over correctly."""
    expected_values = [EnvironmentStatus.INACTIVE, EnvironmentStatus.ACTIVE]
    actual_values = list(EnvironmentStatus)
    assert actual_values == expected_values, (
        f"Expected {expected_values}, got {actual_values}."
    )


def test_event_scheduler_status_names():
    """Verify the names of the EnvironmentStatus members."""
    assert EnvironmentStatus.INACTIVE.name == "INACTIVE", (
        "The name of INACTIVE should be 'INACTIVE'."
    )
    assert EnvironmentStatus.ACTIVE.name == "ACTIVE", (
        "The name of ACTIVE should be 'ACTIVE'."
    )


def test_event_scheduler_status_str_representation():
    """Ensure the string representation of EnvironmentStatus members is correct."""
    assert str(EnvironmentStatus.INACTIVE) == "inactive", (
        "String representation of INACTIVE is incorrect."
    )
    assert str(EnvironmentStatus.ACTIVE) == "active", (
        "String representation of ACTIVE is incorrect."
    )
