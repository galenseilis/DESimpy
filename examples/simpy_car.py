from desimpy.des import Event, EventScheduler


# Define the car process
def car(env: EventScheduler) -> None:
    """The car process."""
    print(f"Start parking at {env.current_time}")

    def end_parking_action() -> None:
        print(f"Start driving at {env.current_time}")
        env.timeout(2, action=lambda: car(env))

    env.timeout(5, end_parking_action)


# Initialize the event scheduler
scheduler = EventScheduler()

# Schedule the car process to start at time 0
scheduler.timeout(0, action=lambda: car(scheduler))

# Run the simulation
scheduler.run_until_max_time(15)
