"""
```yaml
contents:
    - 0. Imports
    - 1. Configuration
    - 2. Define Counter Resource
    - 3. Define Customer Class
    - 4. Define Bank Class
    - 5. Initialize Event Scheduler
    - 6. Initialize Counter
    - 7. Register Processes
    - 8. Run Simulation
source: https://simpy.readthedocs.io/en/stable/examples/bank_renege.html
```
"""

##############
# $0 IMPORTS #
##############

import random

from desimpy import Event, EventScheduler

####################
# $1 CONFIGURATION #
####################

RANDOM_SEED = 42
NEW_CUSTOMERS = 5  # Total number of customers
INTERVAL_CUSTOMERS = 10.0  # Generate new customers roughly every x seconds
MIN_PATIENCE = 1  # Min. customer patience
MAX_PATIENCE = 3  # Max. customer patience
COUNTER_CAPACITY = 1  # Num. customers that can be served in parallel
TIME_IN_BANK = 12.0  # Time spent in bank
random.seed(RANDOM_SEED)

##############################
# $2 DEFINE COUNTER RESOURCE #
##############################


class Counter:
    """
    A resource representing the bank counter with limited capacity.

    Attributes:
        env (EventScheduler): The event scheduler.
        capacity (int): Number of concurrent customers the counter can serve.
        available (int): Number of available spots at the counter.
        queue (list): Queue of customers waiting to be served.
    """

    def __init__(self, env: EventScheduler, capacity: int) -> None:
        self.env = env
        self.capacity = capacity
        self.available = capacity
        self.queue = []

    def request(self, customer):
        """
        Request service for a customer. If there's space, they will be served immediately,
        otherwise, they join the queue.
        """
        if self.available > 0:
            self.available -= 1
            self.env.schedule(Event(self.env.current_time, customer.start_service))
        else:
            self.queue.append(customer)
            print(f"{customer.name} is waiting at {self.env.current_time}")

    def release(self):
        """
        Release a spot when a customer finishes service. If there are customers in the queue,
        schedule the next one to be served.
        """
        self.available += 1
        if self.queue:
            next_customer = self.queue.pop(0)
            self.request(next_customer)


############################
# $3 DEFINE CUSTOMER CLASS #
############################


class Customer:
    """
    Represents a customer arriving at the bank, with a limited patience.

    Attributes:
        env (EventScheduler): The event scheduler.
        name (str): Name of the customer.
        counter (Counter): The bank counter.
        patience (float): Maximum time the customer is willing to wait.
        time_in_bank (float): Time the customer needs for service.
    """

    def __init__(
        self, env: EventScheduler, name: str, counter: Counter, time_in_bank: float
    ):
        self.env = env
        self.name = name
        self.counter = counter
        self.patience = random.uniform(MIN_PATIENCE, MAX_PATIENCE)
        self.time_in_bank = time_in_bank
        self.arrive_time = self.env.current_time
        print(f"{self.arrive_time:.4f} {self.name}: Here I am")
        self.env.schedule(Event(self.arrive_time, self.check_patience))

    def check_patience(self):
        """
        Check if the customer can be served before their patience runs out.
        """
        self.counter.request(self)
        # Schedule reneging event based on the patience
        self.env.schedule(Event(self.env.current_time + self.patience, self.renege))

    def start_service(self):
        """
        Start the service at the counter and schedule the finish event.
        """
        wait_time = self.env.current_time - self.arrive_time
        print(f"{self.env.current_time:.4f} {self.name}: Waited {wait_time:.3f}")
        service_time = random.expovariate(1.0 / self.time_in_bank)
        self.env.schedule(
            Event(self.env.current_time + service_time, self.finish_service)
        )

    def finish_service(self):
        """
        Finish the service and leave the bank.
        """
        print(f"{self.env.current_time:.4f} {self.name}: Finished")
        self.counter.release()

    def renege(self):
        """
        Reneges if the customer has not been served before their patience runs out.
        """
        if self in self.counter.queue:
            self.counter.queue.remove(self)
            wait_time = self.env.current_time - self.arrive_time
            print(
                f"{self.env.current_time:.4f} {self.name}: RENEGED after {wait_time:.3f}"
            )


########################
# $4 DEFINE BANK CLASS #
########################


class Bank:
    """
    Simulate the bank, generating customers at random intervals and handling their service.
    """

    def __init__(self, env: EventScheduler, counter: Counter):
        self.env = env
        self.counter = counter

    def generate_customers(
        self, num_customers: int, interval: float, time_in_bank: float
    ):
        """
        Generate customers at random intervals.
        """
        for i in range(num_customers):
            arrival_time = random.expovariate(1.0 / interval)
            self.env.schedule(
                Event(
                    self.env.current_time + arrival_time,
                    lambda i=i: Customer(
                        self.env, f"Customer{i:02d}", self.counter, time_in_bank
                    ),
                )
            )


if __name__ == "__main__":
    #################################
    # $5 INITIALIZE EVENT SCHEDULER #
    #################################

    scheduler = EventScheduler()

    #########################
    # $6 INITIALIZE COUNTER #
    #########################

    counter = Counter(scheduler, capacity=COUNTER_CAPACITY)

    #########################
    # $7 REGISTER PROCESSES #
    #########################

    bank = Bank(scheduler, counter)
    bank.generate_customers(
        NEW_CUSTOMERS, INTERVAL_CUSTOMERS, time_in_bank=TIME_IN_BANK
    )

    #####################
    # $8 RUN SIMULATION #
    #####################

    scheduler.run_until_max_time(float("inf"), logging=False)
