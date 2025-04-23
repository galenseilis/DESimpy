###########
# IMPORTS #
###########

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Callable
    from typing import Any, Final

from simdist import dists

from desimpy import EventScheduler, Event

#########################
# DEFINE CUSTOMER CLASS #
#########################


class Customer:
    """Class representing a customer in the queueing system."""

    def __init__(self, customer_id: int, arrival_time: float):
        """Initialize a new Customer instance.

        Args:
            customer_id (int): Unique identifier for the customer.
            arrival_time (float): Time at which the customer arrives.

        """
        self.customer_id: int = customer_id
        self.arrival_time: float = arrival_time
        self.service_start_time: float | None = None
        self.departure_time: float | None = None


#############################
# DEFINE G/G/c Queue System #
#############################


class GGcQueue:
    """Simulation of a G/G/c queueing system."""

    def __init__(
        self,
        arrival_dist: dists.Distribution,
        service_dist: dists.Distribution,
        num_servers: int,
        max_time: float,
    ) -> None:
        """Initialize a G/G/c queueing system.

        Args:
            arrival_dist (dists.Distribution): Distribution for inter-arrival times.
            service_dist (dists.Distribution): Distribution for service times.
            num_servers (int): Number of servers.
            max_time (float): Maximum simulation time.

        """
        self.arrival_dist: dists.Distribution = arrival_dist
        self.service_dist: dists.Distribution = service_dist
        self.num_servers: int = num_servers  # c (number of servers)
        self.max_time: float = max_time  # Max simulation time
        self.scheduler: EventScheduler = EventScheduler()  # Event scheduler
        self.queue: list[Customer] = []  # Queue for customers
        self.servers: list[Customer | None] = [
            None,
        ] * self.num_servers  # Track server status
        self.total_customers: int = 0  # Total customers processed
        self.total_wait_time: float = 0.0  # Accumulated wait time

    def schedule_arrival(self) -> None:
        """Schedule the next customer arrival.

        The time until the next arrival is sampled from the arrival distribution.
        """
        """Schedule the next customer arrival."""
        inter_arrival_time: float = self.arrival_dist.sample()
        action = lambda: self.handle_arrival()
        context = {"type": "arrival", "schedule_time": self.scheduler.current_time}
        self.scheduler.timeout(inter_arrival_time, action, context=context)

    def handle_arrival(self) -> None:
        """Handle a customer arrival event.

        If a server is available, the customer immediately begins service.
        Otherwise, they join the queue. The next arrival is also scheduled.
        """
        customer: Customer = Customer(self.total_customers, self.scheduler.current_time)
        self.total_customers += 1

        free_server: int | None = self.find_free_server()

        if free_server is not None:
            self.start_service(customer, free_server)
        else:
            self.queue.append(customer)

        self.schedule_arrival()  # Schedule the next arrival

    def find_free_server(self) -> int | None:
        """Find an available server.

        Returns:
            int | None: The index of a free server, or None if all servers are busy.

        """
        for i in range(self.num_servers):
            if self.servers[i] is None:
                return i
        return None

    def start_service(self, customer: Customer, server_id: int) -> None:
        """Start service for a customer at a specific server.

        Args:
            customer (Customer): The customer to serve.
            server_id (int): The index of the server that will serve the customer.

        """
        service_time: float = self.service_dist.sample()
        customer.service_start_time = self.scheduler.current_time
        self.servers[server_id] = customer  # Mark the server as busy

        action: Callable[[], None] = lambda: self.handle_departure(server_id)
        context: dict[str, Any] = {
            "type": "handle_departure",
            "schedule_time": self.scheduler.current_time,
            "server": server_id,
            "customer_id": customer.customer_id,
        }
        # Schedule the departure event

        self.scheduler.timeout(service_time, action=action, context=context)

    def handle_departure(self, server_id: int) -> None:
        """Handle the departure of a customer from a server.

        Frees the server and starts service for the next customer in the queue if one exists.

        Args:
            server_id (int): The index of the server where the departure occurred.

        """
        """Handle the departure of a customer from a given server."""
        customer: Customer | None = self.servers[server_id]
        assert customer is not None
        customer.departure_time = self.scheduler.current_time
        self.servers[server_id] = None  # Free the server

        assert customer.service_start_time is not None
        wait_time: float = customer.service_start_time - customer.arrival_time
        self.total_wait_time += wait_time

        if self.queue:
            next_customer = self.queue.pop(0)
            self.start_service(next_customer, server_id)

    def run(self) -> list[Event]:
        """Run the G/G/c queue simulation.

        Returns:
            list[Event]: A log of events that occurred during the simulation.

        """
        self.schedule_arrival()  # Schedule the first arrival
        return self.scheduler.run_until_max_time(self.max_time)  # Run until max_time


# Example usage of the simulation
if __name__ == "__main__":
    ########################
    # CONFIGURE SIMULATION #
    ########################

    arrival_dist: dists.Distribution = dists.Gamma(1, 2)
    service_dist: dists.Distribution = dists.Gamma(2, 1)
    num_servers: Final[int] = 2  # Number of servers
    max_time: Final[float] = 100.0  # Maximum simulation time

    #########################
    # INITIALIZE SIMULATION #
    #########################

    simulation: GGcQueue = GGcQueue(arrival_dist, service_dist, num_servers, max_time)

    ##################
    # RUN SIMULATION #
    ##################

    event_log: list[Event] = simulation.run()

    ###################
    # PRINT EVENT LOG #
    ###################

    for event in event_log:
        print(event.time, event.context)
