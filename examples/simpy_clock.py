from desimpy.des import EventScheduler


def clock(env, name, tick) -> None:
    """Clock simulation process."""

    def action() -> None:
        """Schedule next tick of the clock."""
        print(name, env.current_time)
        env.timeout(tick, action)

    env.timeout(0, action=action)


# Setting up the simulation environment
env = EventScheduler()

# Scheduling the 'fast' and 'slow' clocks
clock(env, "fast", 0.5)
clock(env, "slow", 1)

# Running the simulation until time 2
env.run_until_max_time(2)
