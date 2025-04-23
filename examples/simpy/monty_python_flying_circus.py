"""
source: https://simpy.readthedocs.io/en/stable/topical_guides/environments.html#simulation-control
"""

#############
# $ IMPORTS #
#############

from desimpy import Event, EventScheduler

################################
# $ INITIALIZE EVENT SCHEDULER #
################################

env = EventScheduler()

##################
# $ DEFINE EVENT #
##################

my_proc = Event(1, lambda: "Monty Python’s Flying Circus")

####################
# $ REGISTER EVENT #
####################

env.schedule(my_proc)

####################
# $ RUN SIMULATION #
####################

_ = env.run_until_given_event(my_proc)
