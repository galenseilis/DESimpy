# Overview

DESimpy is a library that provides a minimalist set of components for implementing discrete event simulations.

# Quickstart

Install using pip:

```bash
pip install desimpy
```

Now you can prepare a short example like this one:

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

