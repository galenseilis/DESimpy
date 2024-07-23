from desimpy.des import Event, EventScheduler, stop_at_max_time_factory
import heapq


class Car:
    def __init__(self, env: EventScheduler) -> None:
        self.env = env
        self.interrupted = False
        self.schedule_run()

    def schedule_run(self) -> None:
        """Schedule the initial run event."""
        start_time = self.env.current_time
        self.env.schedule(Event(start_time, self.run))

    def run(self) -> None:
        """Handle the parking and charging, followed by driving."""
        print(f"Start parking and charging at {self.env.current_time}")

        charge_duration = 5
        end_charge_time = self.env.current_time + charge_duration

        def charge_action() -> None:
            if not self.interrupted:
                print(f"Start driving at {self.env.current_time}")
                trip_duration = 2
                end_trip_time = self.env.current_time + trip_duration

                # Schedule the next parking and charging event
                self.env.schedule(Event(end_trip_time, self.run))
            else:
                print(f"Was interrupted. Hope, the battery is full enough ...")
                self.interrupted = False
                # Resume driving after interruption
                self.env.schedule(Event(self.env.current_time, self.run))

        # Schedule the charge process
        self.env.schedule(Event(end_charge_time, charge_action))

    def interrupt(self) -> None:
        """Interrupt the current charging process."""
        self.interrupted = True


def driver(env: EventScheduler, car: Car) -> None:
    """Driver process that interrupts the car."""
    interrupt_time = env.current_time + 3

    def interrupt_action() -> None:
        car.interrupt()

    env.schedule(Event(interrupt_time, interrupt_action))


# Initialize the event scheduler
scheduler = EventScheduler()

# Create a car instance
car = Car(scheduler)

# Schedule the driver process
scheduler.schedule(Event(0, lambda : driver(scheduler, car)))

# Define the stop condition
stop_condition = stop_at_max_time_factory(15)

# Run the simulation
scheduler.run(stop_condition)
