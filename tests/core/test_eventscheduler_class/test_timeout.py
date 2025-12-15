from desimpy import Environment


def test_event_with_context():
    delay = 10
    action = lambda: 2018
    context = {"foo": "bar", 1: "baz"}
    env = Environment()
    env.timeout(delay=delay, action=action, context=context)
    event_out = env.step()
    assert event_out.time == 10
    assert event_out.action() == 2018
    assert event_out.context == context
    event_result: int = event_out.result
    assert event_result == 2018
