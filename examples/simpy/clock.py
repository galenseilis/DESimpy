"""SimPy Clock Example

source: https://simpy.readthedocs.io/en/stable/index.html#overview
"""

from desimpy import Environment


def clock(env: Environment, name: str, tick: float) -> None:
    """Simulates a clock process that prints the current simulation time at regular intervals.

    The clock ticks at the specified interval and prints its name along with the
    current simulation time. This process continues until the simulation ends.

    Args:
        env (Environment): The simulation environment responsible for
            scheduling and managing events.
        name (str): The name of the clock, which will be printed at each tick.
        tick (float): The interval in time units between each tick of the clock.

    """

    def action() -> None:
        """Schedules the next tick of the clock.

        Prints the clock's name and the current simulation time, and schedules
        the next tick to occur after the specified interval.
        """
        print(name, env.current_time)
        env.timeout(tick, action)

    env.timeout(0, action=action)


if __name__ == "__main__":
    env = Environment()
    clock(env, "fast", 0.5)
    clock(env, "slow", 1)
    _ = env.run_until_max_time(2, logging=True)
