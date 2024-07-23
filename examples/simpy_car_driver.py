from desimpy.des import EventScheduler

class Car:
    def __init__(self, env: EventScheduler) -> None:
        self.env = env
        self.interrupted = False
        self.schedule_run()

    def schedule_run(self) -> None:
        """Schedule the initial run event."""
        self.env.timeout(0, self.run)

    def run(self) -> None:
        """Handle the parking and charging, followed by driving."""
        print(f"Start parking and charging at {self.env.current_time}")

        def charge_action() -> None:
            if not self.interrupted:
                print(f"Start driving at {self.env.current_time}")

                # Schedule the next parking and charging event
                self.env.timeout(2, self.run)
            else:
                print(f"Was interrupted. Hope, the battery is full enough ...")
                self.interrupted = False
                # Resume driving after interruption
                self.env.timeout(0, self.run)

        # Schedule the charge process
        self.env.timeout(5, charge_action)

    def interrupt(self) -> None:
        """Interrupt the current charging process."""
        self.interrupted = True


def driver(env: EventScheduler, car: Car) -> None:
    """Driver process that interrupts the car."""

    def interrupt_action() -> None:
        car.interrupt()

    env.timeout(3, interrupt_action)


# Initialize the event scheduler
scheduler = EventScheduler()

# Create a car instance
car = Car(scheduler)

# Schedule the driver process
scheduler.timeout(0, lambda: driver(scheduler, car))

# Run the simulation
scheduler.run_until_max_time(15)
