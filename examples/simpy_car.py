"""
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

##############
# $0 IMPORTS #
##############

from desimpy.des import Event, EventScheduler

#########################
# $1 DEFINE CAR PROCESS #
#########################


def car(env: EventScheduler) -> None:
    """The car process."""
    print(f"Start parking at {env.current_time}")

    def end_parking_action() -> None:
        print(f"Start driving at {env.current_time}")
        env.timeout(2, action=lambda: car(env))

    env.timeout(5, end_parking_action)


#################################
# $2 INITIALIZE EVENT SCHEDULER #
#################################

scheduler = EventScheduler()

###########################
# $3 SCHEDULE CAR PROCESS #
###########################

scheduler.timeout(0, action=lambda: car(scheduler))

#####################
# $4 RUN SIMULATION #
#####################

scheduler.run_until_max_time(15, logging=False)
