from desimpy.des import Event, EventScheduler, stop_at_max_time_factory


class Car:
    def __init__(self, env: EventScheduler) -> None:
        self.env = env
        # Start the run process when an instance is created
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

        # Define the action to be executed when charging ends
        def charge_action() -> None:
            print(f"Start driving at {self.env.current_time}")
            trip_duration = 2
            end_trip_time = self.env.current_time + trip_duration

            # Schedule the next parking and charging event
            self.env.schedule(Event(end_trip_time, self.run))

        # Schedule the charge process
        self.env.schedule(Event(end_charge_time, charge_action))


# Initialize the event scheduler
scheduler = EventScheduler()

# Create a car instance
Car(scheduler)

# Define the stop condition
stop_condition = stop_at_max_time_factory(15)

# Run the simulation
scheduler.run(stop_condition)
