"""Simpy clock example."""


def run_simpy():
    """Simpy implementation."""
    import simpy

    results: list[tuple[str, float]] = []

    def clock(env: simpy.Environment, name: str, tick: float):
        while True:
            results.append((name, env.now))
            yield env.timeout(tick)

    env = simpy.Environment()

    _ = env.process(clock(env, "fast", 0.5))
    _ = env.process(clock(env, "slow", 1))

    _ = env.run(until=2)

    return results


def run_desimpy():
    """DESimpy implementation."""
    from desimpy import Environment

    results: list[tuple[str, float]] = []

    def clock(env: Environment, name: str, tick: float) -> None:
        def action() -> None:
            results.append((name, env.current_time))
            env.timeout(tick, action)

        env.timeout(0, action=action)

    env = Environment()
    clock(env, "fast", 0.5)
    clock(env, "slow", 1)
    _ = env.run_until_max_time(2, logging=False)

    return results


def test_equal_histories():
    """Compare histories of distinct implementations."""
    assert run_simpy() == run_desimpy()
