def run_simpy():
    import simpy

    results = []

    def clock(env, name, tick):
        while True:
            results.append((name, env.now))
            yield env.timeout(tick)

    env = simpy.Environment()

    env.process(clock(env, "fast", 0.5))
    env.process(clock(env, "slow", 1))

    env.run(until=2)

    return results


def run_desimpy():
    from desimpy import Event, EventScheduler

    results = []

    def clock(env: EventScheduler, name: str, tick: float) -> None:
        def action() -> None:
            results.append((name, env.current_time))
            env.timeout(tick, action)

        env.timeout(0, action=action)

    env = EventScheduler()
    clock(env, "fast", 0.5)
    clock(env, "slow", 1)
    env.run_until_max_time(2, logging=False)

    return results


def test_equal_histories():
    assert run_simpy() == run_desimpy()
