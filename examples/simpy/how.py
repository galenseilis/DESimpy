"""source: https://simpy.readthedocs.io/en/stable/topical_guides/simpy_basics.html#best-practice-version-of-the-example-above"""

from collections.abc import Callable

from desimpy import Environment


def example(env: Environment) -> None:
    """Example function that schedules an action in a simulation environment.

    This function defines an action that prints the current time in the environment
    along with a hardcoded value of 42. It schedules this action to occur after a
    timeout of 1 unit of time.

    Args:
        env (desimpy.Environment): The simulation environment in which the action is scheduled.

    Returns:
        None: This function does not return a value, it schedules an event.

    """
    delay = 1
    value = 42
    action: Callable[[], None] = lambda: print(f"now={env.current_time}, {value=}")
    env.timeout(delay, action)


if __name__ == "__main__":
    env = Environment()
    example(env)
    env.run_until_max_time(float("inf"), logging=False)
