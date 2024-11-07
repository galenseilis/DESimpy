import random

from desimpy import EventScheduler


class Customer:
    """Class representing a customer in the queueing system."""

    def __init__(self, customer_id, arrival_time):
        self.customer_id = customer_id
        self.arrival_time = arrival_time
        self.service_start_time = None
        self.departure_time = None


class MMcQueueSimulation:
    def __init__(self, arrival_rate, service_rate, num_servers, max_time):
        self.arrival_rate = arrival_rate  # λ (arrival rate)
        self.service_rate = service_rate  # μ (service rate)
        self.num_servers = num_servers  # c (number of servers)
        self.max_time = max_time  # Max simulation time
        self.scheduler = EventScheduler()  # Event scheduler
        self.queue = []  # Queue for customers
        self.servers = [None] * self.num_servers  # Track server status
        self.total_customers = 0  # Total customers processed
        self.total_wait_time = 0.0  # Accumulated wait time

    def schedule_arrival(self):
        """Schedule the next customer arrival."""
        inter_arrival_time = random.expovariate(1 / self.arrival_rate)
        self.scheduler.timeout(
            inter_arrival_time,
            lambda: self.handle_arrival(),
            context={"type": "arrival", "schedule_time": self.scheduler.current_time},
        )

    def handle_arrival(self):
        """Handle a customer arrival."""
        customer = Customer(self.total_customers, self.scheduler.current_time)
        self.total_customers += 1

        free_server = self.find_free_server()

        if free_server is not None:
            self.start_service(customer, free_server)
        else:
            self.queue.append(customer)

        self.schedule_arrival()  # Schedule the next arrival

    def find_free_server(self):
        """Find an available server."""
        for i in range(self.num_servers):
            if self.servers[i] is None:
                return i
        return None

    def start_service(self, customer, server_id):
        """Start service for a customer at a given server."""
        service_time = random.expovariate(1 / self.service_rate)
        customer.service_start_time = self.scheduler.current_time
        self.servers[server_id] = customer  # Mark the server as busy

        # Schedule the departure event

        self.scheduler.timeout(
            service_time,
            lambda: self.handle_departure(server_id),
            context={
                "type": "handle_departure",
                "schedule_time": self.scheduler.current_time,
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

    def run(self):
        """Run the M/M/c queue simulation."""
        self.schedule_arrival()  # Schedule the first arrival
        return self.scheduler.run_until_max_time(self.max_time)  # Run until max_time


# Example usage of the simulation
if __name__ == "__main__":
    arrival_rate = 7.0  # Average arrival rate
    service_rate = 1 / 2  # Average service rate
    num_servers = 2  # Number of servers
    max_time = 100.0  # Maximum simulation time

    simulation = MMcQueueSimulation(arrival_rate, service_rate, num_servers, max_time)

    results = simulation.run()
    for result in results:
        print(result.context)
