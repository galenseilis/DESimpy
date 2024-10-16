"""
```yaml
source: https://simpy.readthedocs.io/en/stable/topical_guides/environments.html#simulation-control
contents:
    - 0. Imports
    - 1. Initialize Event Scheduler
    - 2. Define Event
    - 3. Register Event
    - 4. Run Simulation
```
"""

##############
# $0 IMPORTS #
##############

from desimpy.des import Event, EventScheduler

#################################
# $1 INITIALIZE EVENT SCHEDULER #
#################################

env = EventScheduler()

###################
# $2 DEFINE EVENT #
###################

my_proc = Event(1, lambda: "Monty Python’s Flying Circus")

#####################
# $3 REGISTER EVENT #
#####################

env.schedule(my_proc)

#####################
# $4 RUN SIMULATION #
#####################

env.run_until_event(my_proc)[0][1]
