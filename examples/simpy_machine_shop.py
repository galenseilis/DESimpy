"""```yaml
contents:
    - 0. Imports
    - 1. Configuration
    - 2. Define General Functions
    - 3. Define Machine Class
    - 4. Define Repairman
    - 5. Define Other Jobs
    - 6. Initialize Event Scheduler
    - 7. Register Processes
    - 8. Run Simulation
    - 9. Show Results
source: https://simpy.readthedocs.io/en/stable/examples/machine_shop.html#machine-shop
```
"""

##############
# $0 IMPORTS #
##############

import heapq
import random
from typing import Any

from desimpy import Event, EventScheduler

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


def time_per_part() -> float:
    """Samples the duration of time required to complete a part.

    This function generates a time value based on a truncated normal distribution with a mean and standard deviation defined in the configuration. The value is truncated at zero to ensure positive time.

    Returns:
        float: The sampled time for completing a part.
    """
    t = random.normalvariate(PT_MEAN, PT_SIGMA)
    while t <= 0:
        t = random.normalvariate(PT_MEAN, PT_SIGMA)
    return t


def time_to_failure() -> float:
    """Samples the time until the next machine failure.

    This function generates a failure time following an exponential distribution
    based on the mean time to failure (MTTF) defined in the configuration.

    Returns:
        float: The sampled time to the next machine failure.
    """
    return random.expovariate(BREAK_MEAN)


###########################
# $3 DEFINE MACHINE CLASS #
###########################


class Machine:
    """Represents a machine in the shop that processes parts and can break down.

    Each machine works on parts and can fail at random intervals, requiring a repairman
    to fix it. The machine class manages the part processing and failure events.

    Attributes:
        env (EventScheduler): The event scheduler managing simulation events.
        name (str): The name or identifier of the machine.
        parts_made (int): The total number of parts made by the machine.
        broken (bool): The status of the machine (True if broken, False if working).
        time_to_part (float): The remaining time to complete the current part.
        part_start_time (float): The start time of the current part.
        current_job (Event): The currently scheduled job (either part processing or repair).
        repairman (Repairman): The repairman responsible for fixing the machine when it breaks.
    """

    def __init__(self, env, name: Any, repairman) -> None:
        """Initializes a machine instance.

        Args:
            env (EventScheduler): The event scheduler for handling events.
            name (str): The identifier or name of the machine.
            repairman (Repairman): The repairman responsible for repairs.
        """
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

    def working(self, back_to_work: bool = False) -> None:
        """Starts working on a part.

        If a part is already being worked on, it resumes from where it left off
        before any interruptions (such as a breakdown). Otherwise, a new part
        begins processing.

        Args:
            back_to_work (bool): Indicates whether the machine is resuming work after a breakdown.
        """
        self.time_to_part = (
            time_per_part() if not self.time_to_part else self.time_to_part
        )

        self.current_job = Event(
            self.env.current_time + self.time_to_part,
            self.complete_part,
            {"machine": self, "type": "working"},
        )

        self.env.schedule(self.current_job)

    def complete_part(self) -> None:
        """Completes the current part and begins working on the next part.

        This method increments the part count and schedules the next part to be processed.
        """
        self.parts_made += 1
        self.time_to_part = 0
        self.working()

    def gonna_break(self) -> None:
        """Schedules a machine breakdown event based on a sampled failure time.

        This method uses the time-to-failure function to determine when the machine
        will break down and schedules an event accordingly.
        """
        time_to_break = time_to_failure()
        self.env.timeout(time_to_break, self.break_machine)

    def break_machine(self) -> None:
        """Handles the machine breaking down.

        When the machine breaks, it halts the current part processing, and a request
        is sent to the repairman for repair.
        """
        self.broken = True

        self.current_job.deactivate()
        self.time_to_part = self.current_job.time - self.env.current_time

        self.repairman.request(self, 1)


#######################
# $4 DEFINE REPAIRMAN #
#######################


class Repairman:
    """Manages the repair and handling of machine breakdowns.

    The repairman class handles repair requests from machines and can be preempted
    to prioritize more urgent tasks. It uses a priority queue to manage job requests.

    Attributes:
        env (EventScheduler): The event scheduler managing simulation events.
        requestor_queue (list): The priority queue of repair requests.
        current_priority (float): The priority of the currently active job.
        current_job (Event): The currently assigned repair job.
    """

    def __init__(self, env: EventScheduler) -> None:
        """Initializes a repairman instance.

        Args:
            env (EventScheduler): The event scheduler managing simulation events.
        """
        self.env = env
        self.requestor_queue = []
        self.current_priority = float("inf")
        self.current_job = None

    def request(self, requestor: Any, request_priority: int) -> None:
        """Processes a repair or other job request.

        This method either schedules a new job if no current job is active,
        or adds the request to the queue if it has a lower priority.

        Args:
            requestor (Machine or callable): The machine or job requesting service.
            request_priority (int): The priority of the request (lower value is higher priority).
        """
        if self.current_job is None:
            self.schedule_job(requestor, request_priority)
        else:
            if self.will_preempt(request_priority):
                self.interrupt_job()
                self.schedule_job(requestor, request_priority)
            else:
                self.schedule_request(requestor, request_priority)

    def schedule_job(self, requestor: Any, priority: int) -> None:
        """Schedule a new job for the repairman.

        Creates a new job for the given requestor with the specified priority and
        schedules it using the event scheduler. This method also assigns the newly
        created job as the current job being processed by the repairman.

        Args:
            requestor (Machine or Callable): The entity requesting the job, either a
            machine that needs repair or another process.
            priority (int): The priority of the job request. Lower values indicate higher priority.
        """
        job = self.create_job(requestor, priority)
        self.assign_current_job(job, priority)
        self.env.schedule(job)

    def assign_current_job(self, job: Event, job_priority: int):
        """Assign the given job as the current job being processed.

        Updates the repairman's state to reflect that the given job is the active job
        being worked on. The priority of the current job is also updated accordingly.

        Args:
            job (Event): The job event to assign as the current job.
            job_priority (int): The priority of the assigned job.
        """
        self.current_job = job
        self.current_priority = job_priority

    def create_job(self, requestor: Any, request_priority: int):
        """Create a new job event for the given requestor.

        Generates a new job event with a scheduled service time, action, and context.
        The service time is calculated based on the job's priority. The job action
        is to call the `complete_job` method upon completion.

        Args:
            requestor (Machine or Callable): The entity requesting the job.
            request_priority (int): The priority of the job, where 1 indicates the highest urgency.

        Returns:
            Event: A new event representing the scheduled job with its assigned time and context.
        """
        service_time = self.job_time(requestor)
        time = self.env.current_time + service_time
        action = self.complete_job
        context = {"requestor": requestor, "priority": request_priority}
        return Event(time, action, context)

    def complete_job(self) -> None:
        """Completes the current job and processes the next job in the queue, if any.

        This method updates the machine's status when repairs are complete or handles
        other types of jobs if scheduled.
        """
        requestor = self.current_job.context.get("requestor", None)
        priority = self.current_priority
        self.current_job = None
        self.current_priority = None
        if priority == 1:
            requestor.broken = False
            requestor.working(back_to_work=True)
            requestor.gonna_break()
        else:
            requestor(self)

        if self.requestor_queue:
            new_priority, _, new_requestor = heapq.heappop(self.requestor_queue)
            self.schedule_job(new_requestor, new_priority)

    def job_time(self, request_priority: int) -> None:
        """Calculate the time required to complete a job.

        Determines the duration of a job based on the priority of the request.
        If the request is a high-priority machine repair (priority=1), the job takes
        a fixed `REPAIR_TIME`. For lower priority jobs (priority>1), a different
        duration (`JOB_DURATION`) is used.

        Args:
            request_priority (int): The priority of the job, where 1 is the highest
            priority (machine repair), and higher values indicate lower-priority jobs.

        Returns:
            float: The time (in minutes) required to complete the job.
        """
        if request_priority == 1:
            delay = REPAIR_TIME
        else:
            delay = JOB_DURATION
        return delay

    def will_preempt(self, priority: int) -> None:
        """Check if a new request should preempt the current job.

        Determines if the new request with a given priority should interrupt the
        currently ongoing job based on the priority comparison. Lower priority values
        signify higher urgency.

        Args:
            priority (int): The priority of the new request, where 1 is the highest.

        Returns:
            bool: True if the new request should preempt the current job, False otherwise.
        """
        return priority < self.current_priority

    def interrupt_job(self) -> None:
        """Interrupt the current job and reschedule it.

        Deactivates the currently running job and pushes it back into the request
        queue with the same priority it had originally, so it can be resumed after
        handling a more urgent job.
        """
        self.current_job.deactivate()
        old_requestor = self.current_job.context["requestor"]
        old_priority = self.current_job.context["priority"]
        self.schedule_request(old_requestor, old_priority)

    def schedule_request(self, requestor, priority) -> None:
        """Add a job request to the repairman's queue.

        Inserts a new job request into the requestor queue with its assigned priority,
        maintaining the priority-based order in the queue.

        Args:
            requestor (Machine or Callable): The entity requesting the job, either a
            machine or another process.
            priority (int): The priority of the job request. Lower values indicate higher priority.
        """
        heapq.heappush(
            self.requestor_queue, (priority, self.env.current_time, requestor)
        )


########################
# $5 DEFINE OTHER JOBS #
########################


def other_jobs(repairman: Repairman):
    """Generates other miscellaneous tasks for the repairman to handle.

    This function submits a job with lower priority, such as maintenance or other tasks,
    to keep the repairman busy when machines are not broken.

    Args:
        repairman (Repairman): The repairman responsible for handling the job.
    """
    repairman.request(other_jobs, 2)


if __name__ == "__main__":
    #################################
    # $6 INITIALIZE EVENT SCHEDULER #
    #################################

    env = EventScheduler()

    #########################
    # $7 REGISTER PROCESSES #
    #########################

    repairman = Repairman(env)
    machines = [Machine(env, i, repairman) for i in range(NUM_MACHINES)]
    env.timeout(0, lambda: other_jobs(repairman))

    #####################
    # $8 RUN SIMULATION #
    #####################

    env.run_until_max_time(SIM_TIME, logging=False)

    ###################
    # $9 SHOW RESULTS #
    ###################

    print("Machine shop")
    print(f"Machine shop results after {WEEKS} weeks")
    for machine in machines:
        print(f"{machine.name} made {machine.parts_made} parts.")
