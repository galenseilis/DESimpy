"""
```yaml
contents:
    - 0. Imports
    - 1. Interrupt by Deactivation
    - 2. Interrupt by Cancellation
```
"""

##############
# $0 IMPORTS #
##############

from desimpy import Event, EventScheduler

if __name__ == "__main__":
    ################################
    # $1 INTERRUPT BY DEACTIVATION #
    ################################

    print("INTERRUPT BY DEACTIVATION")
    env = EventScheduler()

    env.timeout(5, lambda: "foo", context={"meow": 0})
    env.timeout(0, lambda: env.deactivate_next_event(), context={"hi": "bye"})
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
        env.cancel_next_event()
        return "destroyer of worlds"

    env.timeout(0, interrupt_action, context={"hi": "bye"})
    env.timeout(10, lambda: "bar", context={"woof": 1})

    results = env.run_until_max_time(11)

    for result in results:
        event, outcome = result
        print(event.time, outcome, event.context, event.active)
