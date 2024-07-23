from desimpy.des import EventScheduler, Event, stop_at_max_time_factory


def clock(env, name, tick):
    def action():
        print(name, env.current_time)
        env.schedule(Event(env.current_time + tick, action))

    env.schedule(Event(env.current_time, action))


# Setting up the simulation environment
env = EventScheduler()

# Scheduling the 'fast' and 'slow' clocks
clock(env, "fast", 0.5)
clock(env, "slow", 1)

# Running the simulation until time 2
env.run(stop_at_max_time_factory(2))
