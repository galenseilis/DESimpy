from collections import deque
import random

from desimpy.core import Environment, Event


class Customer:
    """Class representing a customer."""

    def __init__(self, arrival_time: float) -> None:
        self.arrival_time = arrival_time
        self.service_start_time = None
        self.service_time = None


class Arrival(Event):
    """Event representing the arrival of a customer."""

    def execute(self, env: Environment) -> None:
        # Schedule next arrival
        inter_arrival_time = random.expovariate(
            1.0
        )  # Exponential distribution with lambda = 1
        next_arrival_time = env.now + inter_arrival_time
        env.schedule_event(Arrival(next_arrival_time))

        # Create customer and add to queue
        customer = Customer(env.now)
        env.queue.append(customer)

        # If there is an available server, start service immediately
        if env.num_servers_available > 0:
            start_service(env, env.queue[0])

        # Add the arrival event to history
        env.history.append(self)

        print(f"Arrival at time {env.now}, Queue Length: {len(env.queue)}")


def start_service(env: Environment, customer: Customer) -> None:
    """Start service for the given customer."""
    customer.service_start_time = env.now
    customer.service_time = random.expovariate(
        1.0
    )  # Exponential distribution with lambda = 1
    departure_time = env.now + customer.service_time
    env.schedule_event(Departure(departure_time))

    env.num_servers_available -= 1

    print(
        f"Service started for customer at time {env.now}, Queue Length: {len(env.queue)}"
    )


class Departure(Event):
    """Event representing the departure of a customer."""

    def execute(self, env: Environment) -> None:
        # Check if there are customers in the queue
        if len(env.queue) > 0:
            # Complete service for the customer
            customer = env.queue[0]
            env.queue.popleft()
            env.num_servers_available += 1

            print(f"Departure at time {env.now}, Queue Length: {len(env.queue)}")

            # Check if there are more customers in the queue
            if len(env.queue) > 0:
                start_service(env, env.queue[0])


if __name__ == "__main__":
    # Initialize simulation environment
    env = Environment()
    env.num_servers_available = 1  # Set the number of servers
    env.queue = deque()  # Initialize the queue

    # Schedule the first arrival
    env.schedule_event(Arrival(0))

    # Run the simulation for a specified time
    simulation_time = 10
    env.run(simulation_time)
