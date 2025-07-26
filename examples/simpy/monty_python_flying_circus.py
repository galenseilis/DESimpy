"""
source: https://simpy.readthedocs.io/en/stable/topical_guides/environments.html#simulation-control
"""

if __name__ == "__main__":
    from desimpy import Event, EventScheduler
    env = EventScheduler()
    my_proc = Event(1, lambda: "Monty Python’s Flying Circus")
    env.schedule(my_proc)
    _ = env.run_until_given_event(my_proc)
