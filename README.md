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

Here is a small example to show the basic logic. This example is the simple car process presented in the SimPy documentation.

```python
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
```
