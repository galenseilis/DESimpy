"""Core components of a discrete event simulation (DES)."""

import heapq
from typing import Callable, NoReturn


class Event:
    """DES event.

    Represents a state transition that can be scheduled by the event scheduler.

    The purpose of context is to provide information for two purposes.
    
    The first is provides a general way for events to store "properties" that are 
    specific to the simulation without the implementation of the DES components
    being strongly coupled to them. That facilites events being part of control
    flow in other parts of the simulation while also being relatively isolated.

    The second purpose for `context` is logging information that was true at the
    time that the event was defined. This will often, although not always, be the
    same simulation time as when the event was scheduled.

    The output of `action` is also for logging purposes. It should not be used
    for control flow within the system specific details of the simulation, and 
    its role in the core discrete event simulation implemention is to provide
    additional information to the log filter and be incorporated into the log
    itself. The types of information that are useful to return are details about
    the system being simulated at the time that the event ellapses.

    The `activate` and `deactivate` methods are handles for synchronization tools
    such as semaphores to manage access to simulated resources or services. An
    event can ellapse when it is inactive, or when it is active. If it is active
    then any system specific state transition will occur. If the event is inactive
    when it is run, then it "fizzes out"; nothing will change in the state of your
    simulation.
    """

    def __init__(self, time: float, action: Callable, context: dict) -> NoReturn:
        self.time = time
        self.action = action
        self.context = context
        self.active = True

    def activate(self) -> NoReturn:
        """Activate event."""
        self.active = True

    def deactivate(self) -> NoReturn:
        """Deactivate event."""
        self.active = False

    def run(self):
        """Apply event's state transitions."""
        if self.active:
            return self.action()
        return None

    def __le__(self, other):
        return self.time <= other.time

    def __lt__(self, other):
        return self.time < other.time


class EventScheduler:
    """Run discrete event simulations."""

    def __init__(self) -> NoReturn:
        self.current_time = 0
        self.event_queue = []

    def schedule(self, event) -> NoReturn:
        """Schedule an event on the event queue."""
        heapq.heappush(self.event_queue, (event.time, event))

    def _default_log_filter(self, event, event_result):
        """Keep all events in the event log."""
        return True

    def run(self, stop: Callable, log_filter: Callable = None) -> list:
        """Run the discrete event simulation.
        
        By default every event will be logged, but for some simulations that may
        become an excessive number of events. Storing a large number of events in
        memory that are not of interest can be a waste of computer memory. Thus the
        `log_filter` function provides a way of filtering which events are logged.
        The `log_filter` expects an event, and keeps that event depending on the 
        event itself (e.g. checking what is in context) as well as the result of the
        event (i.e. `event_result`).
        """
        log_filter = self._default_log_filter if log_filter is None else log_filter
        event_log = []
        while not stop(self):
            if not self.event_queue: # Always stop if there are no more events.
                break
            time, event = heapq.heappop(self.event_queue)
            self.current_time = time
            event_result = event.run()
            if log_filter(event, event_result):
                event_log.append((event, event_result))
        return event_log

def stop_at_max_time_factory(max_time: float) -> Callable:
    """Stop function to halt the simulation at a maximum time.

    Define the scheduler first, then call this function on it
    with the desired max_time to get the desired function. Finally,
    call the event scheduler's run method on the function.
    """
    return lambda scheduler: (scheduler.current_time >= max_time or not bool(scheduler.event_queue) or scheduler.event_queue[0][0] >= max_time)
