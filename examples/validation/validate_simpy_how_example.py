def run_simpy():
    import simpy

    results = []

    def example(env):
        event = simpy.events.Timeout(env, delay=1, value=42)
        value = yield event
        results.append("now=%d, value=%d" % (env.now, value))

    env = simpy.Environment()
    example_gen = example(env)
    p = simpy.events.Process(env, example_gen)
    env.run()

    return results


def run_desimpy():
    from typing import Callable
    from desimpy.des import Event, EventScheduler

    results = []

    def example(env: EventScheduler) -> None:
        delay = 1
        value = 42
        action: Callable[[], None] = lambda: results.append(
            f"now={env.current_time}, {value=}"
        )
        env.timeout(delay, action)

    env = EventScheduler()
    example(env)
    env.run_until_max_time(float("inf"), logging=False)

    return results


if __name__ == "__main__":
    assert run_simpy() == run_desimpy()
