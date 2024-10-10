"""
```yaml
contents:
    - 0. Imports
    - 1. Interrupt by Deactivation
    - 2. Interrupt by Cancellation
    - 3. Interrupt by Deactivation and Custom Event
```
"""

##############
# $0 IMPORTS #
##############

from desimpy.des import Event, EventScheduler

################################
# $1 INTERRUPT BY DEACTIVATION #
################################

print("INTERRUPT BY DEACTIVATION")
env = EventScheduler()

env.timeout(5, lambda: "foo", context={"meow": 0})
env.timeout(0, lambda: env.interrupt_next_event(), context={"hi": "bye"})
env.timeout(10, lambda: "bar", context={"woof": 1})

results = env.run_until_max_time(6)

for result in results:
    event, outcome = result
    print(event.time, outcome, event.context, event.active)

################################
# $2 INTERRUPT BY CANCELLATION #
################################

print("\nINTERRUPT BY CANCELLATION")

env = EventScheduler()

env.timeout(5, lambda: "foo", context={"meow": 0})


def interrupt_action():
    env.interrupt_next_event(method="cancel")
    return "destroyer of worlds"


env.timeout(0, interrupt_action, context={"hi": "bye"})
env.timeout(10, lambda: "bar", context={"woof": 1})

results = env.run_until_max_time(6)

for result in results:
    event, outcome = result
    print(event.time, outcome, event.context, event.active)

#################################################
# $3 INTERRUPT BY DEACTIVATION AND CUSTOM EVENT #
#################################################

print("\nINTERRUPT BY DEACTIVATION WITH NEW EVENT")
env = EventScheduler()

env.timeout(5, lambda: "foo", context={"meow": 0})
env.timeout(
    0,
    lambda: env.interrupt_next_event(
        next_event=Event(30, lambda: "hehe, made it!", context={"the": "end"})
    ),
    context={"hi": "bye"},
)
env.timeout(10, lambda: "bar", context={"woof": 1})

results = env.run_until_max_time(100)

for result in results:
    event, outcome = result
    print(event.time, outcome, event.context, event.active)
