"""This script demonstrates a simple car parking and driving process simulation using a custom discrete-event
simulation (DES) framework. It closely follows the basic SimPy example where a car alternates between parking
and driving. The script schedules and executes events, showing how the car switches states after specific
time intervals.

"""

##############
# $0 IMPORTS #
##############
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Final
from desimpy import EventScheduler

####################
# $1 CONFIGURATION #
####################

COMMENT_SECTIONS: Final[str] = """
```yaml
contents:
    - 0. Imports
    - 1. Define Car Process
    - 2. Initialize Event Scheduler
    - 3. Schedule Car Process
    - 4. Run Simulation
source: https://simpy.readthedocs.io/en/stable/simpy_intro/basic_concepts.html
```
"""

#########################
# $2 DEFINE CAR PROCESS #
#########################


def car(env: EventScheduler) -> None:
    """Simulates the car process that alternates between parking and driving.

    The car parks for 5 time units and then drives for 2 time units, after
    which it returns to parking. This process repeats until the simulation ends.

    Args:
        env (EventScheduler): The simulation environment responsible for
            scheduling and managing events.

    """
    print(f"Start parking at {env.current_time}")

    def end_parking_action() -> None:
        """Action to transition the car from parking to driving. After driving for 2
        time units, the car will park again.

        """
        print(f"Start driving at {env.current_time}")
        env.timeout(2, action=lambda: car(env))

    env.timeout(5, end_parking_action)


if __name__ == "__main__":
    #################################
    # $3 INITIALIZE EVENT SCHEDULER #
    #################################

    scheduler = EventScheduler()

    ###########################
    # $4 SCHEDULE CAR PROCESS #
    ###########################

    scheduler.timeout(0, action=lambda: car(scheduler))

    #####################
    # $5 RUN SIMULATION #
    #####################

    _ = scheduler.run_until_max_time(15, logging=False)
