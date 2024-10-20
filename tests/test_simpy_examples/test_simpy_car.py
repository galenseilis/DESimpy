def run_simpy():
    import simpy

    results = []

    def car(env):
        while True:
            results.append("Start parking at %d" % env.now)
            parking_duration = 5
            yield env.timeout(parking_duration)
            results.append("Start driving at %d" % env.now)
            trip_duration = 2
            yield env.timeout(trip_duration)

    env = simpy.Environment()
    env.process(car(env))
    env.run(until=15)

    return results


def run_desimpy():
    from desimpy import Event, EventScheduler

    results = []

    def car(env: EventScheduler) -> None:
        results.append(f"Start parking at {env.current_time}")

        def end_parking_action() -> None:
            results.append(f"Start driving at {env.current_time}")
            env.timeout(2, action=lambda: car(env))

        env.timeout(5, end_parking_action)

    scheduler = EventScheduler()
    scheduler.timeout(0, action=lambda: car(scheduler))
    scheduler.run_until_max_time(15, logging=False)

    return results


def test_equal_histories():
    assert run_simpy() == run_desimpy()
