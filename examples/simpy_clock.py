"""SimPy Clock Example

```yaml
contents:
    - 0. Imports
    - 1. Define Clock Process
    - 2. Initialize Event Scheduler
    - 3. Schedule Initial Events
    - 4. Run Simulation
source: https://simpy.readthedocs.io/en/stable/index.html#overview
```
"""

##############
# $0 IMPORTS #
##############

from desimpy.des import EventScheduler

###########################
# $1 DEFINE CLOCK PROCESS #
###########################


def clock(env: EventScheduler, name: str, tick: float) -> None:
    """
    Simulates a clock process that prints the current simulation time at regular intervals.

    The clock ticks at the specified interval and prints its name along with the 
    current simulation time. This process continues until the simulation ends.

    Args:
        env (EventScheduler): The simulation environment responsible for 
            scheduling and managing events.
        name (str): The name of the clock, which will be printed at each tick.
        tick (float): The interval in time units between each tick of the clock.

    """

    def action() -> None:
        """
        Schedules the next tick of the clock.

        Prints the clock's name and the current simulation time, and schedules 
        the next tick to occur after the specified interval.
        """
        print(name, env.current_time)
        env.timeout(tick, action)

    env.timeout(0, action=action)


#################################
# $2 INITIALIZE EVENT SCHEDULER #
#################################

env = EventScheduler()

##############################
# $3 SCHEDULE INITIAL EVENTS #
##############################

clock(env, "fast", 0.5)
clock(env, "slow", 1)

#####################
# $4 RUN SIMULATION #
#####################

env.run_until_max_time(2, logging=False)
