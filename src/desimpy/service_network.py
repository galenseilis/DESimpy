"""Components for service network simulation."""

from typing import Callable, NoReturn

from .agent import Agent
from .distributions import Distribution
from .des import Event


class Customer(Agent):  # pylint: disable=R0903
    """Customer agent that receives service."""


class Server(Agent):  # pylint: disable=R0903
    """Server agent that provides service."""

    def __init__(self, name: str, schedule: Callable):
        super().__init__(name)
        self.schedule = schedule
        self.nodes = []

    def is_on_duty(self, node) -> bool:
        """Decide if server is on-duty at a given node."""
        return self.schedule(node)


class WorkForce:
    """Manage servers."""

    def __init__(self, allocate_func: Callable) -> NoReturn:
        self.servers = {}
        self.allocations = {}
        self._allocate_func = allocate_func

    def add_server(self, server):
        """Add a server to the workforce."""
        self.servers[server.name] = server

    def remove_server(self, server_name):
        """Remove a server from the workforce."""
        del self.servers[server_name]

    def allocate_server(self, node):
        """Allocate a server to a job."""
        available_servers = {
            server.is_on_duty(node) for server in self.servers.values()
        }
        return self._allocate_func(available_servers)


class Waitlist:
    """Waitlist to keep track of waiters."""

    def __init__(
        self,
        capacity_func: Callable = None,
        baulk_func: Callable = None,
        service_discipline_func=None,
    ):
        self._capacity_func = (
            lambda node: float("inf") if capacity_func is None else capacity_func
        )
        self._baulk_func = lambda node: False if baulk_func is None else baulk_func
        self._service_discipline = (
            lambda node: node.waitlist.queue[0]
            if service_discipline_func is None
            else service_discipline_func
        )
        self.queue = []

    def capacity(self, node) -> int:
        """Get the capacity of the node."""
        return self._capacity_func(node)

    def baulk(self, node) -> bool:
        """Decide whether an event baulks."""
        return self._baulk_func(node)

    def service_discipline(self, node):
        """Service discipline."""
        return self._service_discipline(node)


class Semaphore:
    """Control access to servers."""

    def __init__(self, node):
        self.node = node
        self.currently_serving = 0

    def acquire(self, event):
        """Attempt for event to acquire lock."""
        if self.currently_serving < self.node.waitlist.capacity:
            self.currently_serving += 1
            return True

        if len(self.node.waitlist.queue) < self.node.capacity:
            self.node.waitlist.queue.append(event)

        return False

    def release(self):
        """Release event from queue."""
        if self.node.waitlist.queue:
            next_event = self.node.waitlist.service_discipline(self.node.waitlist.queue)
            self.node.waitlist.queue.remove(next_event)
            next_event.activate()
            return next_event

        self.currently_serving -= 1
        return None


class Node:
    """Node in queueing network."""

    def __init__(
        self,
        name: str,
        waitlist,
        arrival_distribution: Distribution = None,
        service_distribution: Distribution = None,
        routing_func: Callable = None,
    ):  # pylint: disable=R0913
        """Initialize node.

        Args:
            name (str): Name of the node.
            baulking_func (Callable): Function that decides whether customer is rejected from queue.
            capacity_func (Callable): Function that returns the queue capacity.
            arrival_distribution (Distribution): Time-to-arrival distribution.
            service_discipline (Callable): Function that returns which job to complete next.
            service_distribution (Distribution): Time-to-service-completion distribution.
        """
        self.name = name
        self.arrival_distribution = arrival_distribution
        self.waitlist = waitlist
        self.semaphore = Semaphore(self)
        self.service_distribution = service_distribution
        self.routing_function = routing_func

    def schedule_next_arrival(self, scheduler):
        """Schedule when the next task will arrive."""
        if self.arrival_distribution:
            next_arrival_time = (
                scheduler.current_time + self.arrival_distribution.sample()
            )
            arrival_event = Event(
                next_arrival_time, lambda: self.customer_arrival(scheduler), {}
            )
            scheduler.schedule(arrival_event)

    def customer_arrival(self, scheduler):
        """Schedule customer arrival."""
        arrival_time = scheduler.current_time
        print(f"{arrival_time}: Customer arrives at {self.name}.")
        self.schedule_next_arrival(scheduler)

        service_start_event = Event(
            arrival_time, lambda: self.start_service(scheduler), {}
        )
        if not self.semaphore.acquire(service_start_event):
            print(f"{arrival_time}: Customer waits for service at {self.name}.")

    def start_service(self, scheduler):
        """Start a customer's service."""
        if self.service_distribution:
            service_time = self.service_distribution.sample()
            finish_time = scheduler.current_time + service_time
            print(
                f"{scheduler.current_time}:"
                " Customer starts service at {self.name}"
                " for {service_time} units."
            )

            finish_event = Event(
                finish_time, lambda: self.finish_service(scheduler), {}
            )
            scheduler.schedule(finish_event)

    def finish_service(self, scheduler):
        """Complete a service."""
        print(f"{scheduler.current_time}: Customer finishes service at {self.name}.")
        self.semaphore.release()
        next_node = self.routing_function()
        if next_node:
            next_node.customer_arrival(scheduler)


class ServiceNetworkSimulation:
    """Queueing system simulation."""

    def __init__(self, nodes, workforce, scheduler):
        """Initialize service network simulation.

        Args:
            nodes (List[Node]): List of nodes.
            workforce (Workforce): Class instance that manages servers.
            scheduler (EventScheduler): Event scheduler class instance.
        """
        self.nodes = nodes
        for node in self.nodes:
            node.sim = self
        self.scheduler = scheduler
        self.workforce = workforce

        self.agent_count = 0

    def run(self, stop: Callable):
        """Call the event scheduler to run the simulation.

        Args:
        stop (Callable): The termination condition of the simulation.
        """
        for node in self.nodes:
            node.schedule_next_arrival(self.scheduler)
        self.scheduler.run(stop)

    @property
    def current_time(self):
        """Current simulation time."""
        return self.scheduler.current_time

