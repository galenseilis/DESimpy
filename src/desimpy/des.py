"""Core components of a discrete event simulation (DES)."""

import heapq
from typing import Callable, NoReturn


class Event:
    """DES event.

    Represents a state transition that can be scheduled by the event scheduler.
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
            log_entry = self.action(self.context)
            return self.time, log_entry, self.context
        return self.time, None, self.context


class EventScheduler:
    """Run discrete event simulations."""

    def __init__(self) -> NoReturn:
        self.current_time = 0
        self.event_queue = []

    def schedule(self, event) -> NoReturn:
        """Schedule an event on the event queue."""
        heapq.heappush(self.event_queue, (event.time, event))

    def run(self, stop: Callable) -> NoReturn:
        """Run discrete event simulation."""
        while not stop():
            time, event = heapq.heappop(self.event_queue)
            self.current_time = time
            event.run()


def stop_at_max_time_factory(scheduler, max_time):
    """Stop function to halt the simulation at a maximum time.

    Define the scheduler first, then call this function on it
    with the desired max_time to get the desired function. Finally,
    call the event scheduler's run method on the function.
    """
    return lambda: scheduler.current_time >= max_time
