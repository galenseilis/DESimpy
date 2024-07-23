from desimpy.des import EventScheduler


class Car:
    def __init__(self, env: EventScheduler) -> None:
        self.env = env
        # Start the run process when an instance is created
        self.schedule_run()

    def schedule_run(self) -> None:
        """Schedule the initial run event."""
        self.env.timeout(0, self.run)

    def run(self) -> None:
        """Handle the parking and charging, followed by driving."""
        print(f"Start parking and charging at {self.env.current_time}")

        # Define the action to be executed when charging ends
        def charge_action() -> None:
            print(f"Start driving at {self.env.current_time}")

            # Schedule the next parking and charging event
            self.env.timeout(2, self.run)

        # Schedule the charge process
        self.env.timeout(5, charge_action)


# Initialize the event scheduler
scheduler = EventScheduler()

# Create a car instance
Car(scheduler)

# Run the simulation
scheduler.run_until_max_time(15)
