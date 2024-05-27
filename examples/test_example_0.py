import random
from desimpy import core
from typing import List, Optional

class Customer:
    """Represents a customer in the M/M/1 queue."""

    def __init__(self, arrival_time: float) -> None:
        """Initialize a Customer instance.

        Args:
            arrival_time (float): The time at which the customer arrives.
        """
        self.arrival_time = arrival_time
        self.service_start_time: Optional[float] = None
        self.departure_time: Optional[float] = None

    def start_service(self, service_time: float) -> None:
        """Mark the start of service for the customer.

        Args:
            service_time (float): The time at which the service begins.
        """
        self.service_start_time = max(self.arrival_time, service_time)

    def finish_service(self, departure_time: float) -> None:
        """Mark the end of service for the customer.

        Args:
            departure_time (float): The time at which the service ends.
        """
        self.departure_time = departure_time

    def waiting_time(self) -> float:
        """Calculate the waiting time of the customer.

        Returns:
            float: The waiting time of the customer.
        """
        return self.service_start_time - self.arrival_time

class Queue:
    """Represents the queue in the M/M/1 system."""

    def __init__(self) -> None:
        """Initialize a Queue instance."""
        self.customers: List[Customer] = []

    def add_customer(self, customer: Customer) -> None:
        """Add a customer to the queue.

        Args:
            customer (Customer): The customer to be added to the queue.
        """
        self.customers.append(customer)

    def remove_customer(self) -> Optional[Customer]:
        """Remove a customer from the front of the queue.

        Returns:
            Optional[Customer]: The customer removed from the queue, or None if the queue is empty.
        """
        return self.customers.pop(0) if self.customers else None

    def is_empty(self) -> bool:
        """Check if the queue is empty.

        Returns:
            bool: True if the queue is empty, False otherwise.
        """
        return len(self.customers) == 0

    def size(self) -> int:
        """Get the size of the queue.

        Returns:
            int: The number of customers in the queue.
        """
        return len(self.customers)

class DepartureEvent(core.Event):
    """Handles customer departures."""

    def __init__(self, departure_time: float, queue: Queue, service_time: float) -> None:
        """Initialize a DepartureEvent instance.

        Args:
            departure_time (float): The time at which the departure event occurs.
            queue (Queue): The queue associated with the departure event.
            service_time (float): The service time for customers.
        """
        super().__init__(departure_time)
        self.queue = queue
        self.service_time = service_time

    def execute(self, env: core.Environment) -> None:
        """Execute the departure event.

        Args:
            env (core.Environment): The simulation environment.
        """
        customer = self.queue.remove_customer()
        departure_time = self.time + self.service_time
        customer.finish_service(departure_time)
        if not self.queue.is_empty():
            next_customer = self.queue.customers[0]
            next_customer.start_service(departure_time)
            env.schedule_event(DepartureEvent(departure_time, self.queue, self.service_time))

    def __lt__(self, other: "DepartureEvent") -> bool:
        """Comparison method for sorting in the event queue."""
        return self.time < other.time

class ArrivalEvent(core.Event):
    """Handles customer arrivals."""

    def __init__(self, arrival_time: float, queue: Queue, service_time: float) -> None:
        """Initialize an ArrivalEvent instance.

        Args:
            arrival_time (float): The time at which the arrival event occurs.
            queue (Queue): The queue associated with the arrival event.
            service_time (float): The service time for customers.
        """
        super().__init__(arrival_time)
        self.queue = queue
        self.service_time = service_time

    def execute(self, env: core.Environment) -> None:
        """Execute the arrival event.

        Args:
            env (core.Environment): The simulation environment.
        """
        customer = Customer(self.time)
        if self.queue.is_empty():
            customer.start_service(self.time)
            departure_time = self.time + self.service_time
            customer.finish_service(departure_time)
        self.queue.add_customer(customer)
        if len(self.queue.customers) == 1:
            env.schedule_event(DepartureEvent(self.time, self.queue, self.service_time))

    def __lt__(self, other: "ArrivalEvent") -> bool:
        """Comparison method for sorting in the event queue."""
        return self.time < other.time

def exponential_arrival() -> float:
    """Generate exponentially distributed arrival times."""
    return random.expovariate(1)

def run_simulation(service_time: float, end_time: float) -> Queue:
    """Run the M/M/1 queue simulation.

    Args:
        service_time (float): The service time for customers.
        end_time (float): The end time of the simulation.

    Returns:
        Queue: The queue after the simulation completes.
    """
    env = core.Environment()
    queue = Queue()
    initial_arrival_time = exponential_arrival()
    env.schedule_event(ArrivalEvent(initial_arrival_time, queue, service_time))

    # Schedule next arrival events separately
    while initial_arrival_time < end_time:
        initial_arrival_time += exponential_arrival()
        env.schedule_event(ArrivalEvent(initial_arrival_time, queue, service_time))

    env.run(end_time)
    return queue

if __name__ == "__main__":
    service_time = 1.0
    end_time = 100.0
    queue = run_simulation(service_time, end_time)
    if queue.size() > 0:
        average_waiting_time = sum([c.waiting_time() for c in queue.customers]) / queue.size()
        print(f"Average number of customers in the queue: {average_waiting_time}")
    else:
        print("No customers arrived during the simulation.")
