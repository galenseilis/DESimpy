# DESimPy
Event-driven [discrete event simulation](https://en.wikipedia.org/wiki/Discrete-event_simulation) in Python (DESimPy).

## Overview

DESimPy is an event-driven simulation framework based on standard Python and inspired by [SimPy](https://simpy.readthedocs.io/en/latest/).

Processes in DESimPy are defined by methods owned by Python objects inherited from the `Event` abstract base class. These processes can be used to model system-level or component level changes in a modelled system. Such systems might include customers or patients flowing through services, vehicles in traffic, or agents competing in games.

DESimPy implements time-to-event simulation where the next event in a schedule is processed next regardless of the amount of time in the simulated present to that event. This constrasts with "time sweeping" in which a step size is used to increment foreward in time. It is possible to combine time-to-event with time sweeping (see [Palmer & Tian 2021](https://www.semanticscholar.org/paper/Implementing-hybrid-simulations-that-integrate-in-Palmer-Tian/bea73e8d6c828e15290bc4f01c8dd1a4347c46d0)), however this package does not provide any explicit support for that.

## Installation

```bash
pip install desimpy
```

## Quickstart

```python
def stop_at_max_time(scheduler, max_time):
    """Stop function to halt the simulation at a maximum time."""
    return lambda: scheduler.current_time >= max_time

# Example usage:

# Define a simple action function for events
def example_action(context):
    print(f"Event executed with context: {context}")
    return "example_log_entry"

# Create an event scheduler instance
scheduler = EventScheduler()

# Schedule some events
scheduler.schedule(Event(time=1, action=example_action, context={"data": 1}))
scheduler.schedule(Event(time=2, action=example_action, context={"data": 2}))
scheduler.schedule(Event(time=3, action=example_action, context={"data": 3}))

# Define the stop function with a max time of 2.5
stop_function = stop_at_max_time(scheduler, max_time=2.5)

# Run the simulation
scheduler.run(stop_function)

```
