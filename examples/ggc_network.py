import random
from desimpy import EventScheduler


class Gamma:
    def __init__(self, alpha, beta):
        self.alpha = alpha
        self.beta = beta

    def sample(self):
        return random.gammavariate(self.alpha, self.beta)


class Customer:
    """Class representing a customer in the queueing system."""

    def __init__(self, customer_id, arrival_time):
        self.customer_id = customer_id
        self.arrival_time = arrival_time
        self.service_start_time = None
        self.departure_time = None
        self.current_node = None  # Track the current node (queue) for the customer


class GGcQueue:
    def __init__(
        self,
        queue_id,
        arrival_dist,
        service_dist,
        num_servers,
        routing_func,
        depart_dist,
        scheduler,
    ):
        self.queue_id = queue_id
        self.arrival_dist = arrival_dist
        self.service_dist = service_dist
        self.num_servers = num_servers
        self.scheduler = scheduler  # Shared event scheduler for the network
        self.queue = []  # Queue for customers
        self.servers = [None] * self.num_servers  # Track server status
        self.total_customers = 0  # Total customers processed
        self.total_wait_time = 0.0  # Accumulated wait time
        self.routing_func = routing_func  # Function to route customers to other queues
        self.depart_dist = depart_dist

    def schedule_arrival(self, inter_arrival_time=None):
        """Schedule the next customer arrival."""
        if inter_arrival_time is None:
            inter_arrival_time = self.arrival_dist.sample()
        self.scheduler.timeout(
            inter_arrival_time,
            lambda: self.handle_arrival(),
            context={
                "type": "arrival",
                "schedule_time": self.scheduler.current_time,
                "queue_id": self.queue_id,
            },
        )

    def handle_arrival(self):
        """Handle a customer arrival."""
        customer = Customer(self.total_customers, self.scheduler.current_time)
        self.total_customers += 1
        customer.current_node = self.queue_id  # Track the customer's current queue

        free_server = self.find_free_server()

        if free_server is not None:
            self.start_service(customer, free_server)
        else:
            self.queue.append(customer)

        # Schedule the next arrival for the same queue
        self.schedule_arrival()

    def find_free_server(self):
        """Find an available server."""
        for i in range(self.num_servers):
            if self.servers[i] is None:
                return i
        return None

    def start_service(self, customer, server_id):
        """Start service for a customer at a given server."""
        service_time = self.service_dist.sample()
        customer.service_start_time = self.scheduler.current_time
        self.servers[server_id] = customer  # Mark the server as busy

        # Schedule the departure event
        self.scheduler.timeout(
            service_time,
            lambda: self.handle_departure(server_id),
            context={
                "type": "handle_departure",
                "schedule_time": self.scheduler.current_time,
                "queue_id": self.queue_id,
                "server": server_id,
                "customer_id": customer.customer_id,
            },
        )

    def handle_departure(self, server_id):
        """Handle the departure of a customer from a given server."""
        customer = self.servers[server_id]
        customer.departure_time = self.scheduler.current_time
        self.servers[server_id] = None  # Free the server

        wait_time = customer.service_start_time - customer.arrival_time
        self.total_wait_time += wait_time

        if self.queue:
            next_customer = self.queue.pop(0)
            self.start_service(next_customer, server_id)

        # Route the customer to the next queue (or complete their journey)
        next_node = self.routing_func(self)
        if next_node is not None:
            # Route the customer to the next node in the network
            next_node.schedule_arrival(
                inter_arrival_time=self.depart_dist.sample()
            )


class QueueNetwork:
    """Class representing the entire network of queues."""

    def __init__(self, max_time):
        self.scheduler = EventScheduler()  # Global scheduler for the network
        self.queues = []  # List of all queues in the network
        self.max_time = max_time

    def add_queue(self, queue):
        """Add a queue to the network."""
        self.queues.append(queue)

    def run(self):
        """Run the network simulation."""
        # Schedule initial arrivals for each queue
        for queue in self.queues:
            queue.schedule_arrival()
        return self.scheduler.run_until_max_time(self.max_time)


# Routing function example: round-robin routing between two queues
def round_robin_routing(queue):
    if queue.queue_id == 0:
        return network.queues[1]
    elif queue.queue_id == 1:
        return network.queues[0]
    else:
        return None  # No further routing after the second queue


# Example usage of the network simulation
if __name__ == "__main__":
    network = QueueNetwork(max_time=10.0)  # Maximum simulation time

    # Create two queues with different service distributions and add to the network
    arrival_dist = Gamma(1, 2)  # Shared arrival distribution for both queues
    service_dist1 = Gamma(2, 1)  # Service time for the first queue
    service_dist2 = Gamma(3, 1)  # Service time for the second queue
    depart_dist = Gamma(4, 2)  # departure delay distribution for both queues.

    queue1 = GGcQueue(
        queue_id=0,
        arrival_dist=arrival_dist,
        service_dist=service_dist1,
        num_servers=2,
        routing_func=round_robin_routing,
        depart_dist=depart_dist,
        scheduler=network.scheduler,
    )
    queue2 = GGcQueue(
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
    results = network.run()

    # Print results
    for result in results:
        print(result[0].time, result[0].context, result[1])
