import pytest

from desimpy import Event

def test_event_initialization_default():
    """Test event initialization with default action and context."""
    event = Event(time=10.0)

    # Check the event's time
    assert event.time == 10.0

    # Check the default action (which should do nothing)
    assert callable(event.action)
    assert event.action() is None  # The default action returns None

    # Check the default context is an empty dictionary
    assert event.context == {}

    # The event should be active by default
    assert event.active is True

def test_event_initialization_custom():
    """Test event initialization with custom action and context."""
    custom_action = lambda: "custom_action"
    custom_context = {"key": "value"}

    event = Event(time=15.0, action=custom_action, context=custom_context)

    # Check the event's time
    assert event.time == 15.0

    # Check the custom action
    assert callable(event.action)
    assert event.action() == "custom_action"

    # Check the custom context
    assert event.context == {"key": "value"}

    # The event should still be active by default
    assert event.active is True

def test_event_initialization_invalid_time():
    """Test that event initialization raises error with invalid time."""
    with pytest.raises(ValueError):
        Event(time="invalid")  # Time must be a numeric value

def test_event_initialization_invalid_context():
    """Test event initialization with non-dict context."""
    with pytest.raises(ValueError):
        Event(time=10.0, context=["not", "a", "dict"])  # Context must be a dictionary

def test_event_run_without_activation():
    """Test running an event that has been deactivated."""
    custom_action = lambda: "executed"
    event = Event(time=10.0, action=custom_action)
    
    event.active = False  # Manually deactivate the event
    result = event.run()
    
    assert result is None  # Event action should not be executed when inactive

def test_event_comparison_invalid():
    """Test invalid comparison between Event and non-Event."""
    event1 = Event(time=10.0)
    with pytest.raises(AttributeError):
        assert event1 < "invalid"  # Comparing Event with non-Event should raise an error
