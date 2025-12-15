"""`https://simpy.readthedocs.io/en/stable/simpy_intro/process_interaction.html#waiting-for-a-process`."""


def run_simpy():
    """Simpy implementation."""
    import simpy

    results: list[str] = []

    class Car:
        def __init__(self, env: simpy.Environment):
            self.env: simpy.Environment = env
            self.action: simpy.Process = env.process(self.run())

        def run(self):
            while True:
                results.append("Start parking and charging at %d" % self.env.now)
                charge_duration = 5
                yield self.env.process(self.charge(charge_duration))
                results.append("Start driving at %d" % self.env.now)
                trip_duration = 2
                yield self.env.timeout(trip_duration)

        def charge(self, duration: float):
            yield self.env.timeout(duration)

    env = simpy.Environment()
    _ = Car(env)
    _ = env.run(until=15)

    return results


def run_desimpy():
    """DESimpy implementation."""
    from desimpy import Environment

    results: list[str] = []

    class Car:
        def __init__(self, env: Environment) -> None:
            self.env: Environment = env
            self.schedule_run()

        def schedule_run(self) -> None:
            self.env.timeout(0, self.run)

        def run(self) -> None:
            results.append(f"Start parking and charging at {self.env.current_time}")

            def charge_action() -> None:
                results.append(f"Start driving at {self.env.current_time}")
                self.env.timeout(2, self.run)

            self.env.timeout(5, charge_action)

    scheduler = Environment()
    _ = Car(scheduler)
    _ = scheduler.run_until_max_time(15, logging=False)

    return results


def test_equal_histories():
    """Compare histories created by separate implementations."""
    assert run_simpy() == run_desimpy()
