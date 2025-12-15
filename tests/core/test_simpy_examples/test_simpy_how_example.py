from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Generator
    from typing import Any


def run_simpy():
    """Simpy implementation."""
    import simpy

    results: list[str] = []

    def example(env: simpy.Environment) -> Generator[Any, None, None]:
        event: Any = simpy.events.Timeout(env, delay=1, value=42)
        value = yield event
        results.append("now=%d, value=%d" % (env.now, value))

    env: simpy.Environment = simpy.Environment()
    example_gen: Generator[Any, None, None] = example(env)
    _ = simpy.events.Process(env, example_gen)
    _ = env.run()

    return results


def run_desimpy():
    """DESimpy implementation."""
    from collections.abc import Callable

    from desimpy import Environment

    results: list[str] = []

    def example(env: Environment) -> None:
        delay = 1
        value = 42
        action: Callable[[], None] = lambda: results.append(
            f"now={env.current_time}, {value=}",
        )
        env.timeout(delay, action)

    env = Environment()
    example(env)
    _ = env.run_until_max_time(float("inf"), logging=False)

    return results


def test_equal_histories():
    """Compare histories from distinct implementations."""
    assert run_simpy() == run_desimpy()
