'''Core elements of the simulation package.'''

import abc
import heapq
from typing import Any, NoReturn


class Environment:
    """Execution environment for the event-based simulation.


    Time is passed by stepping from event-to-event.
    """

    def __init__(self) -> NoReturn:
        self.event_queue = []
        self._clock = 0
        self.history = []

    def schedule_event(self, event) -> NoReturn:
        """Schedule an event into the event queue.

        Args:
            time (float): Time that event will be scheduled.
            event (Event): Event to be scheduled.
        """
        heapq.heappush(self.event_queue, event)

    def run(self, end_time: float) -> NoReturn:
        """Run the simulation.

        Args:
            end_time (float): Time that the simulation runs until.
        """

        while self.event_queue:
            current_event = heapq.heappop(self.event_queue)
			current_time = current_event.time

            if current_time < end_time:
                self._clock = current_time

                if not current_event.elapsed:
                    current_event.execute(self)
                    current_event.elapsed = True

                heapq.heappush(self.history, current_event)

            else:
                self._clock = end_time
                break

    @property
    def now(self) -> float:
        """Current time."""
        return self._clock


class Event(abc.ABC):
    """ABC for events to be used in simulation."""

    def __init__(self, time: float) -> NoReturn:
        self.time = time
        self.elapsed = False

    @abc.abstractmethod
    def execute(self, env: Environment) -> Any:
        """Execute the event."""
        raise NotImplementedError("Subclasses must implement the `execute` method")

    def __lt__(self, other) -> bool:
        '''Events are ordered by their schedule time.'''
        return self.time < other.time
