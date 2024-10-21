def run_simpy():
    import simpy

    results = []

    class Car(object):
        def __init__(self, env):
            self.env = env
            self.action = env.process(self.run())

        def run(self):
            while True:
                results.append("Start parking and charging at %d" % self.env.now)
                charge_duration = 5
                yield self.env.process(self.charge(charge_duration))
                results.append("Start driving at %d" % self.env.now)
                trip_duration = 2
                yield self.env.timeout(trip_duration)

        def charge(self, duration):
            yield self.env.timeout(duration)

    env = simpy.Environment()
    car = Car(env)
    env.run(until=15)

    return results


def run_desimpy():
    from desimpy import EventScheduler

    results = []

    class Car:
        def __init__(self, env: EventScheduler) -> None:
            self.env = env
            self.schedule_run()

        def schedule_run(self) -> None:
            self.env.timeout(0, self.run)

        def run(self) -> None:
            results.append(f"Start parking and charging at {self.env.current_time}")

            def charge_action() -> None:
                results.append(f"Start driving at {self.env.current_time}")
                self.env.timeout(2, self.run)

            self.env.timeout(5, charge_action)

    scheduler = EventScheduler()
    Car(scheduler)
    scheduler.run_until_max_time(15, logging=False)

    return results


def test_equal_histories():
    assert run_simpy() == run_desimpy()
