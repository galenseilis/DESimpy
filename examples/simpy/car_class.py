"""Implementation of SimPy's Car example."""

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
    - 1. Configuration
    - 2. Define Car Class
    - 3. Initialize Event Scheduler
    - 4. Initialize Car Instance
    - 5. Run Simulation
```
"""

LOGGING: Final[bool] = False
SIMULATION_TIME: Final[float] = 15.0

#######################
# $2 DEFINE CAR CLASS #
#######################


class Car:
    """A car that alternates between parking/charging and driving in a loop within a simulation environment.

    Upon creation, the car is immediately scheduled to begin its first parking and charging process.
    After parking and charging, it drives for a fixed time, and then repeats the cycle indefinitely.

    Attributes:
        env (EventScheduler): The event scheduler that manages simulation events.

    """

    def __init__(self, env: EventScheduler) -> None:
        """Initialize the Car object and schedule the initial run.

        Args:
            env (EventScheduler): The simulation's event scheduler.

        """
        self.env: EventScheduler = env
        # Start the run process when an instance is created
        self.schedule_run()

    def schedule_run(self) -> None:
        """Schedule the initial parking and charging event.

        This method immediately schedules the first `run` event, with a delay of 0,
        meaning the parking and charging process will start at the current simulation time.
        """
        self.env.timeout(0, self.run)

    def run(self) -> None:
        """Handle the parking and charging process, followed by driving.

        When this method is called, the car starts parking and charging. After
        a fixed charging time of 5 units, the car begins driving. The driving lasts
        for a fixed duration of 2 units, after which the cycle repeats.

        Prints:
            A log message indicating the start of parking/charging, followed by a
            message when driving begins.
        """
        print(f"Start parking and charging at {self.env.current_time}")

        # Define the action to be executed when charging ends
        def charge_action() -> None:
            """Action to be performed after the charging period ends.

            Once the charging is complete, the car starts driving, and the next
            parking/charging cycle is scheduled.

            Prints:
                A log message indicating the start of driving.
            """
            print(f"Start driving at {self.env.current_time}")

            # Schedule the next parking and charging event
            self.env.timeout(2, self.run)

        # Schedule the charge process
        self.env.timeout(5, charge_action)


if __name__ == "__main__":
    #################################
    # $3 INITIALIZE EVENT SCHEDULER #
    #################################

    scheduler = EventScheduler()

    ##############################
    # $4 INITIALIZE CAR INSTANCE #
    ##############################

    _ = Car(scheduler)

    #####################
    # $5 RUN SIMULATION #
    #####################

    _ = scheduler.run_until_max_time(SIMULATION_TIME, logging=LOGGING)
