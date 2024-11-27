# Reference

## API Documentation

Coming soon...

## Glossary of Terms

Coming soon...

## Examples

The examples in this section do not have the same pedagogical aims that the tutorials and the guides have. Rather, they only communicate, "this is a thing that you can do" rather than trying to guide you to a particular learning.

### SimPy Examples

We have implemented various examples from the SimPy documentation. They are intended to help communicate to someone already familiar with SimPy how they might equivalently use DESimpy.

#### Bank Renege

```python
"""Implementation of SimPy's Bank Renege example.

source: https://simpy.readthedocs.io/en/stable/examples/bank_renege.html
"""

from __future__ import annotations

import random
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Final

from desimpy import Event, EventScheduler


RANDOM_SEED: Final[int] = 42
NEW_CUSTOMERS: Final[int] = 5  # Total number of customers
INTERVAL_CUSTOMERS: Final[float] = (
    10.0  # Generate new customers roughly every x seconds
)
MIN_PATIENCE: Final[float] = 1.0  # Min. customer patience
MAX_PATIENCE: Final[float] = 3.0  # Max. customer patience
COUNTER_CAPACITY: Final[int] = 1  # Num. customers that can be served in parallel
TIME_IN_BANK: Final[float] = 12.0  # Time spent in bank
random.seed(RANDOM_SEED)



class Counter:
    """A resource representing the bank counter with limited capacity.

    Attributes:
        env (EventScheduler): The event scheduler.
        capacity (int): Number of concurrent customers the counter can serve.
        available (int): Number of available spots at the counter.
        queue (list): Queue of customers waiting to be served.
    """

    def __init__(self, env: EventScheduler, capacity: int) -> None:
        self.env: EventScheduler = env
        self.capacity: int = capacity
        self.available: int = capacity
        self.queue = []

    def request(self, customer):
        """Request service for a customer. If there's space, they will be served immediately,
        otherwise, they join the queue.
        """
        if self.available > 0:
            self.available -= 1
            self.env.schedule(Event(self.env.current_time, customer.start_service))
        else:
            self.queue.append(customer)
            print(f"{customer.name} is waiting at {self.env.current_time}")

    def release(self):
        """Release a spot when a customer finishes service. If there are customers in the queue,
        schedule the next one to be served.
        """
        self.available += 1
        if self.queue:
            next_customer = self.queue.pop(0)
            self.request(next_customer)




class Customer:
    """Represents a customer arriving at the bank, with a limited patience.

    Attributes:
        env (EventScheduler): The event scheduler.
        name (str): Name of the customer.
        counter (Counter): The bank counter.
        patience (float): Maximum time the customer is willing to wait.
        time_in_bank (float): Time the customer needs for service.
    """

    def __init__(
        self, env: EventScheduler, name: str, counter: Counter, time_in_bank: float
    ):
        self.env = env
        self.name = name
        self.counter = counter
        self.patience = random.uniform(MIN_PATIENCE, MAX_PATIENCE)
        self.time_in_bank = time_in_bank
        self.arrive_time = self.env.current_time
        print(f"{self.arrive_time:.4f} {self.name}: Here I am")
        self.env.schedule(Event(self.arrive_time, self.check_patience))

    def check_patience(self):
        """Check if the customer can be served before their patience runs out."""
        self.counter.request(self)
        # Schedule reneging event based on the patience
        self.env.schedule(Event(self.env.current_time + self.patience, self.renege))

    def start_service(self):
        """Start the service at the counter and schedule the finish event."""
        wait_time = self.env.current_time - self.arrive_time
        print(f"{self.env.current_time:.4f} {self.name}: Waited {wait_time:.3f}")
        service_time = random.expovariate(1.0 / self.time_in_bank)
        self.env.schedule(
            Event(self.env.current_time + service_time, self.finish_service)
        )

    def finish_service(self):
        """Finish the service and leave the bank."""
        print(f"{self.env.current_time:.4f} {self.name}: Finished")
        self.counter.release()

    def renege(self):
        """Reneges if the customer has not been served before their patience runs out."""
        if self in self.counter.queue:
            self.counter.queue.remove(self)
            wait_time: float = self.env.current_time - self.arrive_time
            print(
                f"{self.env.current_time:.4f} {self.name}: RENEGED after {wait_time:.3f}"
            )



class Bank:
    """Simulate the bank, generating customers at random intervals and handling their service."""

    # WARN: Not to be confused with `collections.Counter`.
    def __init__(self, env: EventScheduler, counter: Counter):
        self.env: EventScheduler = env
        self.counter: Counter = counter

    def generate_customers(
        self, num_customers: int, interval: float, time_in_bank: float
    ):
        """Generate customers at random intervals."""
        for i in range(num_customers):
            arrival_time = random.expovariate(1.0 / interval)
            self.env.schedule(
                Event(
                    self.env.current_time + arrival_time,
                    lambda i=i: Customer(
                        self.env, f"Customer{i:02d}", self.counter, time_in_bank
                    ),
                )
            )


if __name__ == "__main__":

    scheduler = EventScheduler()
    counter = Counter(scheduler, capacity=COUNTER_CAPACITY)
    bank = Bank(scheduler, counter)
    bank.generate_customers(
        NEW_CUSTOMERS, INTERVAL_CUSTOMERS, time_in_bank=TIME_IN_BANK
    )
    _ = scheduler.run_until_max_time(float("inf"), logging=False)
```

#### Car Class

```python

"""Implementation of SimPy's Car example."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Final

from desimpy import EventScheduler

LOGGING: Final[bool] = False
SIMULATION_TIME: Final[float] = 15.0


class Car:
    """A car that alternates between parking/charging and driving in a loop within a simulation environment.

    Upon creation, the car is immediately scheduled to begin its first parking and charging process.
    After parking and charging, it drives for a fixed time, and then repeats the cycle indefinitely.

    Attributes:
        env (EventScheduler): The event scheduler that manages simulation events.
    """

    def __init__(self, env: EventScheduler) -> None:
        """Initialize the Car object and schedule the initial run.

        Args:
            env (EventScheduler): The simulation's event scheduler.
        """
        self.env: EventScheduler = env
        # Start the run process when an instance is created
        self.schedule_run()

    def schedule_run(self) -> None:
        """Schedule the initial parking and charging event.

        This method immediately schedules the first `run` event, with a delay of 0,
        meaning the parking and charging process will start at the current simulation time.
        """
        self.env.timeout(0, self.run)

    def run(self) -> None:
        """Handle the parking and charging process, followed by driving.

        When this method is called, the car starts parking and charging. After
        a fixed charging time of 5 units, the car begins driving. The driving lasts
        for a fixed duration of 2 units, after which the cycle repeats.

        Prints:
            A log message indicating the start of parking/charging, followed by a
            message when driving begins.
        """
        print(f"Start parking and charging at {self.env.current_time}")

        # Define the action to be executed when charging ends
        def charge_action() -> None:
            """Action to be performed after the charging period ends.

            Once the charging is complete, the car starts driving, and the next
            parking/charging cycle is scheduled.

            Prints:
                A log message indicating the start of driving.
            """
            print(f"Start driving at {self.env.current_time}")

            # Schedule the next parking and charging event
            self.env.timeout(2, self.run)

        # Schedule the charge process
        self.env.timeout(5, charge_action)


if __name__ == "__main__":
    scheduler = EventScheduler()
    _ = Car(scheduler)
    _ = scheduler.run_until_max_time(SIMULATION_TIME, logging=LOGGING)

```

#### Car Driver

```python
from desimpy import Event, EventScheduler

class Car:
    def __init__(self, env: EventScheduler) -> None:
        self.env: EventScheduler = env
        # Start the run process when an instance is created
        self.schedule_run()

    def schedule_run(self) -> None:
        """Schedule the initial run event."""
        self.env.timeout(0, self.schedule_charge)

    def schedule_drive(self) -> None:
        # Define the action to be executed when charging ends
        print(f"Start driving at {self.env.current_time}")

        # Schedule the next parking and charging event
        self.env.timeout(2, self.schedule_charge)

    def schedule_charge(self) -> None:
        """Handle the parking and charging, followed by driving."""
        print(f"Start parking and charging at {self.env.current_time}")

        # Schedule the charge process
        self.env.timeout(5, self.schedule_drive, context={"event_type": "charge"})


def deactivate_next_charge_condition(env: EventScheduler, event: Event) -> bool:
    """Deactivate the charging event."""
    _ = env
    if event.context.get("event_type", None) == "charge":
        return True
    return False


def driver(env: EventScheduler, car: Car) -> None:
    def interrupt_action():
        print("Was interrupted. Hope, the battery is full enough ...")
        env.deactivate_next_event_by_condition(
            condition=deactivate_next_charge_condition
        )
        event = Event(env.current_time, car.schedule_drive)
        env.schedule(event)

    env.timeout(3, interrupt_action)


if __name__ == "__main__":
    scheduler = EventScheduler()
    car = Car(scheduler)
    driver(scheduler, car)
    _ = scheduler.run_until_max_time(15, logging=False)
```

