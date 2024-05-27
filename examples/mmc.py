import random

from desimpy.core import Environment, Event


class Arrival(Event):
    """Event representing the arrival of a customer."""

    def execute(self, env: Environment) -> None:
        # Schedule next arrival
        inter_arrival_time = random.expovariate(
            1.0
        )  # Exponential distribution with lambda = 1
        next_arrival_time = env.now + inter_arrival_time
        env.schedule_event(Arrival(next_arrival_time))

        # Process the arrival
        if env.num_servers_available > 0:
            env.num_servers_available -= 1
            service_time = random.expovariate(
                1.0
            )  # Exponential distribution with lambda = 1
            departure_time = env.now + service_time
            env.schedule_event(Departure(departure_time))
        else:
            env.queue_length += 1

        print(f"Arrival at time {env.now}, Queue Length: {env.queue_length}")


class Departure(Event):
    """Event representing the departure of a customer."""

    def execute(self, env: Environment) -> None:
        # Process the departure
        env.num_servers_available += 1

        print(f"Departure at time {env.now}, Queue Length: {env.queue_length}")

        # Check for remaining customers in the queue
        if env.queue_length > 0:
            env.queue_length -= 1
            service_time = random.expovariate(
                1.0
            )  # Exponential distribution with lambda = 1
            departure_time = env.now + service_time
            env.schedule_event(Departure(departure_time))


if __name__ == "__main__":
    # Initialize simulation environment
    env = Environment()
    env.num_servers_available = 1  # Set the number of servers
    env.queue_length = 0  # Initialize the queue length

    # Schedule the first arrival
    env.schedule_event(Arrival(0))

    # Run the simulation for a specified time
    simulation_time = 10
    env.run(simulation_time)
