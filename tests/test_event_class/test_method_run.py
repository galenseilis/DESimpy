from desimpy import Event

def test_no_action():
    event = Event(2018)
    result = event.run()
    assert result is None

def test_lambda_none():
    event = Event(2018, action=lambda: None)
    result = event.run()
    assert result is None

# TODO: Still more cases to test!
