from desimpy.des import Event, EventScheduler

raise NotImplementedError()

class Resource:
    def __init__(self, env, capacity=1):
        self.env = env
        self.capacity = capacity
        self.queue_size = 0

    def request(self, charge_duration):
        if self.queue_size < self.capacity:
            self.queue_size += 1
            self.env.timeout(charge_duration, self.release)
        else:
            ... # Put on queue to wait

    def release(self):
        self.queue_size -= 1

def drive(env, driving_time):
    env.timeout(driving_time, request)


def car(env, name, bcs, driving_time, charge_duration):
    drive(env, driving_time)
