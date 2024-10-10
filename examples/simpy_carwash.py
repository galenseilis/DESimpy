import itertools
import random

from desimpy.des import Event, EventScheduler

# Constants
RANDOM_SEED = 42
NUM_MACHINES = 2  # Number of machines in the carwash
WASHTIME = 5  # Minutes it takes to clean a car
T_INTER = 7  # Create a car every ~7 minutes
SIM_TIME = 20  # Simulation time in minutes

random.seed(RANDOM_SEED)


class Carwash:
    """
    A carwash that has a limited number of washing machines (NUM_MACHINES).
    It cleans cars in parallel, subject to availability of machines.
    """

    def __init__(self, env: EventScheduler, num_machines: int, washtime: int):
        self.env = env
        self.num_machines = num_machines
        self.available_machines = num_machines
        self.washtime = washtime
        self.queue = []

    def request(self, car):
        """
        Request a machine for washing. If a machine is available, it starts
        the wash immediately; otherwise, the car waits in the queue.
        """
        if self.available_machines > 0:
            self.available_machines -= 1
            print(f"{self.env.current_time:.2f} {car} enters the carwash.")
            self.env.schedule(
                Event(
                    self.env.current_time + self.washtime, lambda: self.finish_wash(car)
                )
            )
        else:
            print(f"{self.env.current_time:.2f} {car} waits in the queue.")
            self.queue.append(car)

    def finish_wash(self, car):
        """
        Called when a car finishes washing. It releases the machine and checks
        if any cars are waiting in the queue to start washing.
        """
        pct_dirt = random.randint(50, 99)
        print(
            f"{self.env.current_time:.2f} Carwash removed {pct_dirt}% of {car}'s dirt."
        )
        print(f"{self.env.current_time:.2f} {car} leaves the carwash.")

        self.available_machines += 1

        if self.queue:
            next_car = self.queue.pop(0)
            self.request(next_car)


class Car:
    """
    A car that arrives at the carwash and waits to be cleaned.
    """

    def __init__(self, env: EventScheduler, name: str, carwash: Carwash):
        self.env = env
        self.name = name
        self.carwash = carwash
        print(f"{self.env.current_time:.2f} {self.name} arrives at the carwash.")
        self.env.schedule(Event(self.env.current_time, lambda: self.enter_carwash()))

    def enter_carwash(self):
        """
        Enter the carwash and request a machine for cleaning.
        """
        self.carwash.request(self.name)


def setup(env: EventScheduler, num_machines: int, washtime: int, t_inter: int):
    """
    Set up the carwash simulation, starting with an initial set of cars and
    generating new cars at random intervals.
    """
    carwash = Carwash(env, num_machines, washtime)
    car_count = itertools.count()

    # Create 4 initial cars
    for _ in range(4):
        Car(env, f"Car {next(car_count)}", carwash)

    # Function to generate cars continuously
    def generate_car():
        next_arrival_time = random.randint(t_inter - 2, t_inter + 2)
        env.schedule(
            Event(env.current_time + next_arrival_time, lambda: create_new_car())
        )

    # Create new car and schedule next one
    def create_new_car():
        Car(env, f"Car {next(car_count)}", carwash)
        generate_car()

    # Start the initial car generation
    generate_car()


# Simulation setup
scheduler = EventScheduler()
setup(scheduler, NUM_MACHINES, WASHTIME, T_INTER)

# Run simulation
scheduler.run_until_max_time(SIM_TIME, logging=False)
