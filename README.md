# DESimpy

A synchronous [discrete event simulation](https://en.wikipedia.org/wiki/Discrete-event_simulation) (DES) framework in Python (DESimpy).

## Overview

DESimPy provides the core components of DES.

Processes in DESimPy are defined by methods owned by Python objects inherited from the `Event` abstract base class. These processes can be used to model system-level or component level changes in a modelled system. Such systems might include customers or patients flowing through services, vehicles in traffic, or agents competing in games.

DESimPy implements time-to-event simulation where the next event in a schedule is processed next regardless of the amount of time in the simulated present to that event. This constrasts with "time sweeping" in which a step size is used to increment foreward in time. It is possible to combine time-to-event with time sweeping (see [Palmer & Tian 2021](https://www.semanticscholar.org/paper/Implementing-hybrid-simulations-that-integrate-in-Palmer-Tian/bea73e8d6c828e15290bc4f01c8dd1a4347c46d0)), however this package does not provide any explicit support for that.

## Installation

```bash
pip install desimpy
```

## Quickstart

Here is a small example to show the basic logic. This example is the simple clock process presented in the [SimPy documentation](https://simpy.readthedocs.io/en/stable/index.html).

```python
from desimpy import EventScheduler

def clock(env: EventScheduler, name: str, tick: int | float) -> None:
    """Clock simulation process."""

    def action() -> None:
        """Schedule next tick of the clock."""
        print(name, env.current_time)
        env.timeout(tick, action)

    env.timeout(0, action=action)

env = EventScheduler()

clock(env, "fast", 0.5)
clock(env, "slow", 1)

event_log = env.run_until_max_time(2)
```

# Design

- Avoid performance overhead of coroutines.
- Do not change the past (i.e. event log should not be changed during simulation).
- Event schedule ordering is purely temporal order of events elapsing.
- Built-in event logging.
    - Can be turned off for better performance.
- Future schedule is mutable to simulate interruptions.
    - Activating events.
    - Deactivating events.
    - Cancelling events.
