def run_simpy():
    import simpy

    results = []

    def car(env, name, bcs, driving_time, charge_duration):
        yield env.timeout(driving_time)
        results.append("%s arriving at %d" % (name, env.now))
        with bcs.request() as req:
            yield req
            results.append("%s starting to charge at %s" % (name, env.now))
            yield env.timeout(charge_duration)
            results.append("%s leaving the bcs at %s" % (name, env.now))

    env = simpy.Environment()
    bcs = simpy.Resource(env, capacity=2)
    for i in range(4):
        env.process(car(env, "Car %d" % i, bcs, i * 2, 5))

    env.run()

    return results


def run_desimpy():
    from desimpy import Event, EventScheduler

    results = []

    class BatteryChargingStation:
        def __init__(self, env: EventScheduler, capacity: int) -> None:
            self.env = env
            self.capacity = capacity
            self.available_spots = capacity
            self.waiting_queue = []

        def request(self, car) -> None:
            if self.available_spots > 0:
                self.available_spots -= 1
                self.env.schedule(Event(self.env.current_time, car.start_charging))
            else:
                self.waiting_queue.append(car)
                results.append(f"{car.name} is waiting at time {self.env.current_time}")

        def release(self) -> None:
            self.available_spots += 1
            if self.waiting_queue:
                next_car = self.waiting_queue.pop(0)
                self.request(next_car)

    class Car:
        def __init__(
            self,
            env: EventScheduler,
            name: str,
            bcs: BatteryChargingStation,
            driving_time: float,
            charge_duration: float,
        ) -> None:
            self.env = env
            self.name = name
            self.bcs = bcs
            self.driving_time = driving_time
            self.charge_duration = charge_duration
            # Schedule the car to arrive after driving_time
            self.env.schedule(
                Event(self.env.current_time + self.driving_time, self.arrive)
            )

        def arrive(self) -> None:
            results.append(f"{self.name} arriving at {self.env.current_time}")
            self.bcs.request(self)

        def start_charging(self) -> None:
            results.append(f"{self.name} starting to charge at {self.env.current_time}")
            # Schedule the car to leave after charging is done
            self.env.schedule(
                Event(self.env.current_time + self.charge_duration, self.leave)
            )

        def leave(self) -> None:
            results.append(f"{self.name} leaving the BCS at {self.env.current_time}")
            self.bcs.release()

    scheduler = EventScheduler()
    bcs = BatteryChargingStation(scheduler, capacity=2)
    for i in range(4):
        Car(scheduler, name=f"Car {i}", bcs=bcs, driving_time=i * 2, charge_duration=5)
    scheduler.run_until_max_time(20, logging=False)

    return results


def test_equal_histories():
    run_simpy() == run_desimpy()
