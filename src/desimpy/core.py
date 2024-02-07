import abc
import heapq
import random
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
        heapq.heappush(self.event_queue, (event.time, event))

    def run(self, end_time: float) -> NoReturn:
        """Run the simulation.

        Args:
            end_time (float): Time that the simulation runs until.
        """

        while self.event_queue:
            current_time, current_event = heapq.heappop(self.event_queue)

            if current_time < end_time:
                self._clock = current_time

                if not current_event.elapsed:
                    current_event.execute()
                    current_event.elapsed = True

                heapq.heappush(self.history, (current_time, current_event))

            else:
                self._clock = end_time
                break

    @property
    def now(self) -> float:
        """Current time."""
        return self._clock


class Event(abc.ABC):
    """An event to be used in simulation."""

    def __init__(self, env: Environment, time: float) -> NoReturn:
        self.env = env
        self.time = time
        self.elapsed = False

    def schedule_next(self, time_delta: float) -> NoReturn:
        """Schedule the next time this event occurs.

        Args:
            time_delta (float): Time when this event will re-occur.
        """
        if time_delta < 0:
            raise ValueError(f"Variable `time_delta = {time_delta}` must be non-negative.")

        self.env.schedule_event(self.time + time_delta, self)

    @abc.abstractmethod
    def execute(self) -> Any:
        """Execute the event."""
        raise NotImplementedError("Subclasses must implement the `execute` method")
