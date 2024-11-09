"""`https://simpy.readthedocs.io/en/latest/simpy_intro/process_interaction.html#waiting-for-a-process`."""
from __future__ import annotations


def run_simpy() -> list[str]:
    """Simpy implementation."""
    import simpy

    results: list[str] = []

    def driver(env: simpy.Environment, car:Car):
        yield env.timeout(3)
        car.action.interrupt()

    class Car:
        def __init__(self, env: simpy.Environment):
            self.env: simpy.Environment = env
            self.action: simpy.Process = env.process(self.run())

        def run(self):
            while True:
                results.append("Start parking and charging at %d" % self.env.now)
                charge_duration = 5
                try:
                    yield self.env.process(self.charge(charge_duration))
                except simpy.Interrupt:
                    results.append(
                        "Was interrupted. Hope, the battery is full enough ..."
                    )

                results.append("Start driving at %d" % self.env.now)
                trip_duration = 2
                yield self.env.timeout(trip_duration)

        def charge(self, duration: float):
            yield self.env.timeout(duration)

    env = simpy.Environment()
    car = Car(env)
    _ = env.process(driver(env, car))
    _ = env.run(until=15)
    return results


def run_desimpy() -> list[str]:
    """DESimpy equivalent of Simpy simulation."""
    from desimpy import Event, EventScheduler

    results: list[str] = []

    class Car:
        def __init__(self, env: EventScheduler) -> None:
            self.env: EventScheduler = env
            self.schedule_run()

        def schedule_run(self) -> None:
            self.env.timeout(0, self.schedule_charge)

        def schedule_drive(self) -> None:
            results.append(f"Start driving at {self.env.current_time}")
            self.env.timeout(2, self.schedule_charge)

        def schedule_charge(self) -> None:
            results.append(f"Start parking and charging at {self.env.current_time}")
            self.env.timeout(5, self.schedule_drive)

    def driver(env: EventScheduler, car: Car) -> None:
        def interrupt_action():
            results.append("Was interrupted. Hope, the battery is full enough ...")
            env.deactivate_next_event()
            event = Event(env.current_time, car.schedule_drive)
            env.schedule(event)

        env.timeout(3, interrupt_action)

    scheduler = EventScheduler()
    car = Car(scheduler)
    driver(scheduler, car)
    _ = scheduler.run_until_max_time(15, logging=False)
    return results


def test_equal_histories():
    """Compare histories generated by distinct implementations."""
    assert run_simpy() == run_desimpy()
