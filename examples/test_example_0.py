import random
from desimpy import core

class Customer:
    """Represents a customer in the M/M/1 queue."""

    def __init__(self, arrival_time):
        self.arrival_time = arrival_time
        self.service_start_time = None
        self.departure_time = None

    def start_service(self, service_time):
        self.service_start_time = max(self.arrival_time, service_time)

    def finish_service(self, departure_time):
        self.departure_time = departure_time

    def waiting_time(self):
        return self.service_start_time - self.arrival_time

class Queue:
    """Represents the queue in the M/M/1 system."""

    def __init__(self):
        self.customers = []

    def add_customer(self, customer):
        self.customers.append(customer)

    def remove_customer(self):
        return self.customers.pop(0) if self.customers else None

    def is_empty(self):
        return len(self.customers) == 0

    def size(self):
        return len(self.customers)

class DepartureEvent(core.Event):
    """Handles customer departures."""

    def __init__(self, departure_time, queue, service_time):
        super().__init__(departure_time)
        self.queue = queue
        self.service_time = service_time

    def execute(self, env):
        customer = self.queue.remove_customer()
        departure_time = self.time + self.service_time
        customer.finish_service(departure_time)
        if not self.queue.is_empty():
            next_customer = self.queue.customers[0]
            next_customer.start_service(departure_time)
            env.schedule_event(DepartureEvent(departure_time, self.queue, self.service_time))

    def __lt__(self, other):
        """Comparison method for sorting in the event queue."""
        return self.time < other.time

class ArrivalEvent(core.Event):
    """Handles customer arrivals."""

    def __init__(self, arrival_time, queue, service_time):
        super().__init__(arrival_time)
        self.queue = queue
        self.service_time = service_time

    def execute(self, env):
        customer = Customer(self.time)
        if self.queue.is_empty():
            customer.start_service(self.time)
            departure_time = self.time + self.service_time
            customer.finish_service(departure_time)
        self.queue.add_customer(customer)
        if len(self.queue.customers) == 1:
            env.schedule_event(DepartureEvent(self.time, self.queue, self.service_time))

    def __lt__(self, other):
        """Comparison method for sorting in the event queue."""
        return self.time < other.time

def exponential_arrival():
    return random.expovariate(1)

def run_simulation(service_time, end_time):
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

