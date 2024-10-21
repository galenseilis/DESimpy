import pytest
from desimpy import Event


def test_compare_with_str():
    event = Event(2018)
    with pytest.raises(AttributeError, match="'str' object has no attribute 'time'"):
        assert event <= "foo"


def test_compare_with_int():
    event = Event(2018)
    with pytest.raises(AttributeError, match="'int' object has no attribute 'time'"):
        assert event <= 2019


def test_compare_with_tuple():
    event = Event(2018)
    with pytest.raises(AttributeError, match="'tuple' object has no attribute 'time'"):
        assert event <= ()


def test_compare_with_list():
    event = Event(2018)
    with pytest.raises(AttributeError, match="'list' object has no attribute 'time'"):
        assert event <= []


def test_expected_order():
    event1 = Event(0)
    event2 = Event(1)
    event3 = Event(2)

    assert event1 <= event2
    assert event2 <= event3
    assert event1 <= event3
