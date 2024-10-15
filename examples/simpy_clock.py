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
    """Clock simulation process."""

    def action() -> None:
        """Schedule next tick of the clock."""
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
