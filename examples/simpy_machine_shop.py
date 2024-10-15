"""
```yaml
source: https://simpy.readthedocs.io/en/stable/examples/machine_shop.html#machine-shop
```
"""

##############
# $0 IMPORTS #
##############

import copy
import heapq
import random

from desimpy.des import Event, EventScheduler

####################
# $1 CONFIGURATION #
####################

RANDOM_SEED = 2018
PT_MEAN = 10.0
PT_SIGMA = 2.0
MTTF = 300.0
BREAK_MEAN = 1 / MTTF
REPAIR_TIME = 30.0
JOB_DURATION = 30.0
NUM_MACHINES = 10
WEEKS = 4
SIM_TIME = WEEKS * 7 * 24 * 60

###############################
# $2 DEFINE GENERAL FUNCTIONS #
###############################


def time_per_part():
    """Sample duration of time to complete a part."""
    t = random.normalvariate(PT_MEAN, PT_SIGMA)
    while t <= 0:
        t = random.normalvariate(PT_MEAN, PT_SIGMA)
    return t


def time_to_failure():
    """Sample time until next machine failure."""
    return random.expovariate(BREAK_MEAN)


###########################
# $3 DEFINE MACHINE CLASS #
###########################


class Machine:
    def __init__(self, env, name, repairman):
        self.env = env
        self.name = name
        self.parts_made = 0
        self.broken = False
        self.time_to_part = 0
        self.part_start_time = None
        self.current_job = None
        self.repairman = repairman

        self.working()
        self.gonna_break()

    def working(self, back_to_work=False):
        """Start working on a part."""

        self.time_to_part = (
            time_per_part() 
            if not self.time_to_part 
            else self.time_to_part
        )

        self.current_job = Event(
            self.env.current_time + self.time_to_part,
            self.complete_part,
            {"machine": self, "type": "working"},
        )

        self.env.schedule(self.current_job)

    def complete_part(self):
        """Update state to reflect part completion."""
        self.parts_made += 1
        self.time_to_part = 0
        self.working()

    def gonna_break(self):
        """Schedule machine breaking."""
        time_to_break = time_to_failure()
        self.env.timeout(time_to_break, self.break_machine)

    def break_machine(self):
        """Break machine!"""

        # Set status to "broken".
        self.broken = True

        self.current_job.deactivate()
        self.time_to_part = self.current_job.time - self.env.current_time
        assert self.current_job.time - self.env.current_time


        # Send a request to the repairman to fix.
        self.repairman.request(self, 1)


#######################
# $4 DEFINE REPAIRMAN #
#######################


class Repairman:
    """The man that repairs machines, and assorted tasks as assigned."""

    def __init__(self, env):
        self.env = env
        self.requestor_queue = []
        self.current_priority = float("inf")
        self.current_job = None

    def request(self, requestor, request_priority):
        """Process a request."""
        if self.current_job is None:
            self.schedule_job(requestor, request_priority)
        else:
            if self.will_preempt(request_priority):
                self.interrupt_job()
                self.schedule_job(requestor, request_priority)
            else:
                print(self.env.current_time)
                self.schedule_request(requestor, request_priority)

    def schedule_job(self, requestor, priority):
        job = self.create_job(requestor, priority)
        self.assign_current_job(job, priority)
        self.env.schedule(job)

    def assign_current_job(self, job, job_priority):
        self.current_job = job
        self.current_priority = job_priority

    def create_job(self, requestor, request_priority):
        """Create a job to schedule."""
        service_time = self.job_time(requestor)
        time = self.env.current_time + service_time
        action = self.complete_job
        context = {"requestor": requestor, "priority": request_priority}
        return Event(time, action, context)

    def complete_job(self):
        """Transitions for job complete."""
        requestor = self.current_job.context.get("requestor", None)
        priority = self.current_priority
        self.current_job = None
        self.current_priority = None
        if priority == 1:
            requestor.broken = False
            requestor.working(back_to_work=True)
            requestor.gonna_break()

        if self.requestor_queue:
            new_priority, _, new_requestor = heapq.heappop(self.requestor_queue)
            self.schedule_job(new_requestor, new_priority)

    def job_time(self, request_priority):
        """How long it takes to finish the job."""
        if request_priority == 1:
            delay = REPAIR_TIME
        else:
            delay = JOB_DURATION
        return delay

    def will_preempt(self, priority):
        return priority < self.current_priority

    def interrupt_job(self):
        self.current_job.deactivate()
        old_requestor = self.current_job.context["requestor"]
        old_priority = self.current_job.context["priority"]
        self.schedule_request(old_requestor, old_priority)

    def schedule_request(self, requestor, priority):
        heapq.heappush(self.requestor_queue, (priority, self.env.current_time, requestor))


########################
# $5 DEFINE OTHER JOBS #
########################


def other_jobs(env, repairman):
    ...


##################
# RUN SIMULATION #
##################

print("Machine shop")

env = EventScheduler()
repairman = Repairman(env)
machines = [Machine(env, i, repairman) for i in range(NUM_MACHINES)]
results = env.run_until_max_time(SIM_TIME)

################
# SHOW RESULTS #
################

print(f"Machine shop results after {WEEKS} weeks")
for machine in machines:
    print(f"{machine.name} made {machine.parts_made} parts.")
