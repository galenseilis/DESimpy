from desimpy import Environment


def test_default():
    """Test that an Environment is correctly initialized."""
    scheduler = Environment()

    # Test if current_time is set to 0
    assert scheduler.current_time == 0

    # Test if event_queue is an empty list
    assert scheduler.event_queue == []

    # Test if event_log is an empty list
    assert scheduler.event_log == []
