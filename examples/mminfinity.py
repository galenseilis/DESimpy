import random
import math

from desimpy.core import Environment, Event

class Arrival(Event):
    """Event representing the arrival of a customer."""

    def execute(self, env: Environment) -> None:
        # Schedule next arrival
        inter_arrival_time = random.expovariate(1.0)  # Exponential distribution with lambda = 1
        next_arrival_time = env.now + inter_arrival_time
        env.schedule_event(Arrival(next_arrival_time))

        # Process the arrival
        if len(env.history) == 0:
            service_time = random.expovariate(1.0)  # Exponential distribution with lambda = 1
            departure_time = env.now + service_time
            env.schedule_event(Departure(departure_time))
        
        # Add the arrival event to history
        env.history.append(self)

        print(f"Arrival at time {env.now}")

class Departure(Event):
    """Event representing the departure of a customer."""

    def execute(self, env: Environment) -> None:
        # Process the departure
        env.history.append(self)

        print(f"Departure at time {env.now}")

        # Check for remaining customers in the queue
        if len(env.event_queue) > 0:
            service_time = random.expovariate(1.0)  # Exponential distribution with lambda = 1
            departure_time = env.now + service_time
            env.schedule_event(Departure(departure_time))

if __name__ == "__main__":
    # Initialize simulation environment
    env = Environment()

    # Schedule the first arrival
    env.schedule_event(Arrival(0))

    # Run the simulation for a specified time
    simulation_time = 10
    env.run(simulation_time)

