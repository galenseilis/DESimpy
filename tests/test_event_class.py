import pytest

from desimpy.des import Event

class TestEvent:
    
    def test_event_initialization(self):
        """Test event initialization with default and custom parameters."""
        # Default action and context
        event1 = Event(time=10.0)
        assert event1.time == 10.0
        assert callable(event1.action)
        assert event1.action() is None  # Default action does nothing
        assert event1.context == {}  # Default context is an empty dict
        assert event1.active is True

        # Custom action and context
        custom_action = lambda: "custom_action"
        custom_context = {"key": "value"}
        event2 = Event(time=15.0, action=custom_action, context=custom_context)
        assert event2.time == 15.0
        assert event2.action() == "custom_action"
        assert event2.context == {"key": "value"}
        assert event2.active is True

    def test_event_activate(self):
        """Test the activate method."""
        event = Event(time=10.0)
        event.deactivate()  # Initially deactivate it
        assert event.active is False
        event.activate()
        assert event.active is True

    def test_event_deactivate(self):
        """Test the deactivate method."""
        event = Event(time=10.0)
        event.deactivate()
        assert event.active is False

    def test_event_run_active(self):
        """Test that the event's action runs when the event is active."""
        custom_action = lambda: "executed"
        event = Event(time=10.0, action=custom_action)
        assert event.active is True  # By default, event is active
        result = event.run()
        assert result == "executed"  # Action runs and returns the custom result

    def test_event_run_inactive(self):
        """Test that the event's action does not run when the event is inactive."""
        custom_action = lambda: "executed"
        event = Event(time=10.0, action=custom_action)
        event.deactivate()  # Deactivate the event
        assert event.active is False
        result = event.run()
        assert result is None  # Action does not run, returns None

    def test_event_comparison(self):
        """Test the comparison operators (__le__ and __lt__)."""
        event1 = Event(time=5.0)
        event2 = Event(time=10.0)
        event3 = Event(time=5.0)

        assert event1 < event2  # event1 happens before event2
        assert event1 <= event2  # event1 happens before event2
        assert event1 <= event3  # event1 and event3 happen at the same time
        assert event2 > event1  # event2 happens after event1
        assert not (event2 < event1)  # event2 does not happen before event1

