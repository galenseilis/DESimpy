```python
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
