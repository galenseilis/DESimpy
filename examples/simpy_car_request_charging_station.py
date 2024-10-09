"""
```yaml
contents:
    - 0. Imports
    - 1. Define Battery Charging Station
    - 2. Define Car Class
    - 3. Initialize Event Scheduler
    - 4. Initialize Battery Charging Station
    - 5. Register Cars with Scheduler
    - 6. Run Simulation
```
"""

##############
# $0 IMPORTS #
##############

from desimpy.des import Event, EventScheduler

######################################
# $1 DEFINE BATTERY CHARGING STATION #
######################################

class BatteryChargingStation:
    """
    A resource representing a battery charging station with a limited number of charging spots.

    This class models a charging station with a fixed capacity. Cars can request 
    charging spots, and if all spots are occupied, they are placed in a waiting queue.
    
    Attributes:
        env (EventScheduler): The event scheduler that manages simulation events.
        capacity (int): The total number of available charging spots.
        available_spots (int): The number of charging spots currently available.
        waiting_queue (list): A queue for cars waiting for a charging spot.
    """

    def __init__(self, env: EventScheduler, capacity: int) -> None:
        """
        Initialize the BatteryChargingStation with a given capacity.

        Args:
            env (EventScheduler): The simulation's event scheduler.
            capacity (int): The total number of charging spots in the station.
        """
        self.env = env
        self.capacity = capacity
        self.available_spots = capacity
        self.waiting_queue = []

    def request(self, car) -> None:
        """
        Request a charging spot for a car.

        If a charging spot is available, it reduces the available spots by one 
        and schedules the car to start charging. If no spots are available, the 
        car is added to the waiting queue.

        Args:
            car: The car requesting a charging spot.
        """
        if self.available_spots > 0:
            self.available_spots -= 1
            self.env.schedule(Event(self.env.current_time, car.start_charging))
        else:
            self.waiting_queue.append(car)
            print(f"{car.name} is waiting at time {self.env.current_time}")

    def release(self) -> None:
        """
        Release a charging spot after a car finishes charging.

        Increases the number of available spots by one. If any cars are waiting in 
        the queue, the first car in the queue is assigned the newly available spot 
        and its charging process is scheduled.
        """
        self.available_spots += 1
        if self.waiting_queue:
            next_car = self.waiting_queue.pop(0)
            self.request(next_car)

#######################
# $2 DEFINE CAR CLASS #
#######################

class Car:
    """
    A car that uses a battery charging station within a simulation environment.

    Each car has a defined driving time, after which it arrives at the charging 
    station and requests a spot to charge. Once a spot becomes available, the car 
    starts charging for a specific duration, and then leaves the station.

    Attributes:
        env (EventScheduler): The event scheduler that manages simulation events.
        name (str): The name of the car, used for identification in logs.
        bcs (BatteryChargingStation): The battery charging station where the car charges.
        driving_time (float): The amount of time the car spends driving before reaching the station.
        charge_duration (float): The duration for which the car will charge once a spot is available.
    """

    def __init__(
        self,
        env: EventScheduler,
        name: str,
        bcs: BatteryChargingStation,
        driving_time: float,
        charge_duration: float,
    ) -> None:
        """
        Initialize the Car object and schedule its arrival at the charging station.

        Args:
            env (EventScheduler): The simulation's event scheduler.
            name (str): The name of the car.
            bcs (BatteryChargingStation): The battery charging station to use.
            driving_time (float): Time in the simulation before the car arrives at the station.
            charge_duration (float): The amount of time the car will spend charging.
        """
        self.env = env
        self.name = name
        self.bcs = bcs
        self.driving_time = driving_time
        self.charge_duration = charge_duration
        # Schedule the car to arrive after driving_time
        self.env.schedule(Event(self.env.current_time + self.driving_time, self.arrive))

    def arrive(self) -> None:
        """
        Trigger the car's arrival at the charging station.

        Once the car arrives, it requests a charging spot. If one is available, 
        it will be scheduled to start charging; otherwise, it will wait in a queue.

        Prints:
            A log message with the car's name and the current simulation time.
        """
        print(f"{self.name} arriving at {self.env.current_time}")
        self.bcs.request(self)

    def start_charging(self) -> None:
        """
        Start the car's charging process.

        When a charging spot becomes available, the car starts charging. The duration
        of charging is predefined, and after this time, the car will be scheduled to leave.

        Prints:
            A log message with the car's name and the current simulation time.
        """
        print(f"{self.name} starting to charge at {self.env.current_time}")
        # Schedule the car to leave after charging is done
        self.env.schedule(
            Event(self.env.current_time + self.charge_duration, self.leave)
        )

    def leave(self) -> None:
        """
        End the car's charging process and release the charging spot.

        Once the car finishes charging, it leaves the charging station, freeing 
        up a spot for other waiting cars.

        Prints:
            A log message with the car's name and the current simulation time.
        """
        print(f"{self.name} leaving the BCS at {self.env.current_time}")
        self.bcs.release()

#################################
# $3 INITIALIZE EVENT SCHEDULER #
#################################

scheduler = EventScheduler()

##########################################
# $4 INITIALIZE BATTERY CHARGING STATION #
##########################################

bcs = BatteryChargingStation(scheduler, capacity=2)

###################################
# $5 REGISTER CARS WITH SCHEDULER #
###################################

for i in range(4):
    Car(scheduler, name=f"Car {i}", bcs=bcs, driving_time=i * 2, charge_duration=5)

#####################
# $6 RUN SIMULATION #
#####################

scheduler.run_until_max_time(20)
