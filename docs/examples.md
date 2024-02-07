
# SimPy's Clock Example

# SimPy's First Car Example

Let us consider the [first car example](https://simpy.readthedocs.io/en/latest/simpy_intro/basic_concepts.html#our-first-process) from the SimPy documentation. A car alternates between driving and parking for the duration of the simulation. 

```python
# first_car.py
from typing import NoReturn

from desimpy import core

class StartParking(core.Event):
    """Make the car park."""

    def execute(self) -> NoReturn:
        """Start parking and schedule next drive."""

        print(f"Start parking at {self.env.now}")

        scheduled_driving_time = self.env.now + 5

        driving_event = StartDriving(self.env, scheduled_driving_time)

        self.env.schedule_event(driving_event)


class StartDriving(core.Event):
    """Make the car drive."""

    def execute(self) -> NoReturn:
        """Start driving and schedule for next parking."""

        print(f"Start driving at {self.env.now}")

        scheduled_parking_time = self.env.now + 2

        parking_event = StartParking(self.env, scheduled_parking_time)

        self.env.schedule_event(parking_event)


class CarSimulation:
    """Our car simulation."""

    def __init__(self) -> NoReturn:
        self.simulation = core.Environment()

    def run_simulation(self) -> NoReturn:
        arrival_event = StartParking(self.simulation, 0)
        self.simulation.schedule_event(arrival_event)
        self.simulation.run(15)

if __name__ == '__main__':
	example = CarSimulation()
	example.run_simulation()
```

When called as a script it should print the following:

```bash
$ python first_car.py
Start parking at 0
Start driving at 5
Start parking at 7
Start driving at 12
Start parking at 14
```
