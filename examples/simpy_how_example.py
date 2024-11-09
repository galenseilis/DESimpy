"""
```yaml
contents:
    - 0. Imports
    - 1. Define Example Process
    - 2. Intialize Event Scheduler
    - 3. Schedule Example Process
    - 4. Run Simulation
source: https://simpy.readthedocs.io/en/stable/topical_guides/simpy_basics.html#best-practice-version-of-the-example-above
```
"""

##############
# $0 IMPORTS #
##############

from typing import Callable

from desimpy import EventScheduler

#############################
# $1 DEFINE EXAMPLE PROCESS #
#############################


def example(env: EventScheduler) -> None:
    """
    Example function that schedules an action in a simulation environment.

    This function defines an action that prints the current time in the environment
    along with a hardcoded value of 42. It schedules this action to occur after a
    timeout of 1 unit of time.

    Args:
        env (desimpy.EventScheduler): The simulation environment in which the action is scheduled.

    Returns:
        None: This function does not return a value, it schedules an event.
    """
    delay = 1
    value = 42
    action: Callable[[], None] = lambda: print(f"now={env.current_time}, {value=}")
    env.timeout(delay, action)


if __name__ == "__main__":
    #################################
    # $2 INITIALIZE EVENT SCHEDULER #
    #################################

    env = EventScheduler()

    ###############################
    # $3 SCHEDULE EXAMPLE PROCESS #
    ###############################

    example(env)

    #####################
    # $4 RUN SIMULATION #
    #####################

    env.run_until_max_time(float("inf"), logging=False)
