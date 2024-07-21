from desimpy.des import Event, EventScheduler, stop_at_max_time_factory
import heapq

# Define the car process
def car(env: EventScheduler) -> None:
    """The car process."""
    print(f'Start parking at {env.current_time}')
    
    parking_duration = 5
    next_event_time = env.current_time + parking_duration

    def end_parking_action(ctx: dict) -> None:
        print(f'Start driving at {env.current_time}')
        trip_duration = 2
        next_event_time = env.current_time + trip_duration
        
        # Schedule the next parking event
        env.schedule(Event(next_event_time, lambda ctx: car(env), {}))
    
    env.schedule(Event(next_event_time, end_parking_action, {}))

# Initialize the event scheduler
scheduler = EventScheduler()

# Schedule the car process to start at time 0
scheduler.schedule(Event(0, lambda ctx: car(scheduler), {}))

# Define the stop condition
stop_condition = stop_at_max_time_factory(scheduler, 15)

# Run the simulation
scheduler.run(stop_condition)

