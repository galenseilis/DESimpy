from typing import Self
from collections.abc import Callable

# TODO: Pull in simdist package for distributions.
from simdist import dists

from desimpy import EventScheduler


class Customer:
    """Class representing a customer in the queueing system."""

    def __init__(self, customer_id: int, arrival_time: float) -> None:
        self.customer_id: int = customer_id
        self.arrival_time: float = arrival_time
        self.service_start_time: float | None = None
        self.departure_time: float | None = None
        self.current_node: Node | None = (
            None  # Track the current node (queue) for the customer
        )


class Node:
    def __init__(
        self,
        queue_id: int,
        arrival_dist: dists.Distribution,
        service_dist: dists.Distribution,
        num_servers: int,
        routing_func: Callable[[], Self],
        depart_dist: dists.Distribution,
        scheduler: EventScheduler,  # FIX: Provide instance of Network instead, which will have access to scheduler.
    ):
        self.queue_id: int = queue_id
        self.arrival_dist: dists.Distribution = arrival_dist
        self.service_dist: dists.Distribution = service_dist
        self.num_servers: int = num_servers
        self.scheduler: EventScheduler = (
            scheduler  # Shared event scheduler for the network
        )
        self.queue: list[Customer] = []  # Queue for customers
        self.servers: list[Customer | None] = [
            None
        ] * self.num_servers  # Track server status
        self.total_customers: int = (
            0  # FIX: Total number of customers should be tracked by Network.
        )
        self.routing_func: Callable[[], Self] = (
            routing_func  # Function to route customers to other queues
        )
        self.depart_dist: dists.Distribution = depart_dist

    def schedule_arrival(self, inter_arrival_time: float | None = None) -> None:
        """Schedule the next customer arrival."""
        if inter_arrival_time is None:
            inter_arrival_time: float = self.arrival_dist.sample()
        self.scheduler.timeout(
            inter_arrival_time,
            lambda: self.handle_arrival(),
            context={
                "type": "arrival",
                "schedule_time": self.scheduler.current_time,
                "queue_id": self.queue_id,
            },
        )

    def handle_arrival(self):  # FIX: Pass optional customer
        """Handle a customer arrival."""
        customer = Customer(
            self.total_customers, self.scheduler.current_time
        )  # FIX: Create customer only if not provided.
        self.total_customers += 1
        customer.current_node = self.queue_id  # Track the customer's current queue

        free_server = self.find_free_server()

        if free_server is not None:
            self.start_service(customer, free_server)
        else:
            self.queue.append(customer)

        # Schedule the next arrival for the same queue
        self.schedule_arrival()  # FIX: Pass customer

    def find_free_server(self):
        """Find an available server."""
        for i in range(self.num_servers):
            if self.servers[i] is None:
                return i
        return None

    def start_service(self, customer: Customer, server_id: int):
        """Start service for a customer at a given server."""
        service_time: float = self.service_dist.sample()
        customer.service_start_time = self.scheduler.current_time
        self.servers[server_id] = customer  # Mark the server as busy

        action: Callable[[], None] = lambda: self.handle_departure(server_id)
        context = {
            "type": "handle_departure",
            "schedule_time": self.scheduler.current_time,
            "queue_id": self.queue_id,
            "server": server_id,
            "customer_id": customer.customer_id,
        }
        # Schedule the departure event
        self.scheduler.timeout(service_time, action=action, context=context)

    def handle_departure(self, server_id: int):
        """Handle the departure of a customer from a given server."""
        customer = self.servers[server_id]
        customer.departure_time = self.scheduler.current_time
        self.servers[server_id] = None  # Free the server

        wait_time = customer.service_start_time - customer.arrival_time

        if self.queue:
            next_customer = self.queue.pop(0)
            self.start_service(next_customer, server_id)

        # Route the customer to the next queue (or complete their journey)
        next_node: Node | None = self.routing_func(self)
        if next_node is not None:
            # Route the customer to the next node in the network
            next_node.schedule_arrival(  # FIX: Pass customer to be reused.
                inter_arrival_time=self.depart_dist.sample()  # FIX: Pass customer and self to sample
            )


class Network:
    """Class representing the entire network of queues."""

    def __init__(self):
        self.scheduler = EventScheduler()  # Global scheduler for the network
        self.queues = []  # List of all queues in the network

    def add_queue(self, queue):
        """Add a queue to the network."""
        self.queues.append(queue)

    def run(self, max_time):
        """Run the network simulation."""
        # Schedule initial arrivals for each queue
        for queue in self.queues:
            queue.schedule_arrival()
        return self.scheduler.run_until_max_time(max_time)


# Routing function example: round-robin routing between two queues
def round_robin_routing(queue: Node) -> Node | None:
    if queue.queue_id == 0:
        return network.queues[1]
    elif queue.queue_id == 1:
        return network.queues[0]
    else:
        return None  # No further routing after the second queue


# Example usage of the network simulation
if __name__ == "__main__":
    network = Network()  # Maximum simulation time
    # Create two queues with different service distributions and add to the network
    arrival_dist = dists.Gamma(1, 2)  # Shared arrival distribution for both queues
    service_dist1 = dists.Gamma(2, 1)  # Service time for the first queue
    service_dist2 = dists.Gamma(3, 1)  # Service time for the second queue
    depart_dist = dists.Gamma(4, 2)  # departure delay distribution for both queues.

    queue1 = Node(
        queue_id=0,
        arrival_dist=arrival_dist,
        service_dist=service_dist1,
        num_servers=2,
        routing_func=round_robin_routing,
        depart_dist=depart_dist,
        scheduler=network.scheduler,
    )
    queue2 = Node(
        queue_id=1,
        arrival_dist=arrival_dist,
        service_dist=service_dist2,
        num_servers=1,
        routing_func=round_robin_routing,
        depart_dist=depart_dist,
        scheduler=network.scheduler,
    )

    network.add_queue(queue1)
    network.add_queue(queue2)

    # Run the simulation
    event_log = network.run(10)

    # Print results
    for event in event_log:
        print(event.time, event.context, event.result)
