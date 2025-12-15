import heapq
from collections.abc import Callable
from typing import Self

from desimpy.event import Event

EventQueueType = list[tuple[float, Event]]
EventLogType = list[Event]

class EventScheduler:
    """Scheduler for discrete event simulations.
    """

    def __init__(self) -> None:
        """Create an event scheduler."""
        self.event_queue: EventQueueType  = []
        self.event_log: EventLogType  = []


    def schedule(self, event: Event) -> None:
        """Schedule an event on the event queue.

        It is possible to schedule events with negative times
        provided that the current time is zero. In other words,
        before any time has elapsed it is permitted to schedule
        events that occur 'before' t=0. This may be referred to
        as "prescheduling". Sufficient care must be taken by the
        user to ensure that the desired behaviour is achieved with
        prescheduling.
        """
        # OPTIMIZE: Validation checks that are removed when run in optimized mode.
        if __debug__:
            # INFO: Type checker may complain that `event` is always instance of `Event`. Ignore.
            if not isinstance(event, Event):
                # INFO: Type checker may indicate that this code is unreachable, but it is.
                raise TypeError(f"{event=} must be of type Event.")

        heapq.heappush(self.event_queue, (event.time, event))


    def next_event(self) -> Event | None:
        """Refer to next event without changing it."""
        next_pair = heapq.nsmallest(1, self.event_queue)
        if next_pair:
            return next_pair[0][1]
        return None

    def next_event_by_condition(
        self,
        condition: Callable[[Self, Event], bool],
    ) -> Event | None:
        """Return a reference to the next event that satisfies a given condition."""
        for _, event in self.event_queue:
            if condition(self, event):
                return event
        return None

    def peek(self) -> float | None:
        """Get the time of the next event.

        Does not distinguish between active and inactive events.

        Returns infinity if there is no next event.
        """
        next_event = self.next_event()
        if next_event:
            return next_event.time

        return float("inf")

    def peek_by_condition(
        self,
        condition: Callable[[Self, Event], bool],
    ) -> float | None:
        """Return time of next event meeting condition."""
        option_next_event = self.next_event_by_condition(condition)
        if option_next_event:
            return option_next_event.time

    def apply_to_all_events(self, func: Callable[[Event], object]) -> None:
        """Apply a function to all events in schedule."""
        for _, event in self.event_queue:
            func(event)

    def apply_to_events_by_condition(
        self,
        func: Callable[[Event], object],
        condition: Callable[[Self, Event], bool],
    ) -> None:
        """Apply a function to any events in queue that satisfy condition."""
        for _, event in self.event_queue:
            if condition(self, event):
                func(event)

    def activate_next_event(self) -> None:
        """Activate the next scheduled event."""
        option_next_event = self.next_event()
        if option_next_event:
            option_next_event.activate()

    def activate_next_event_by_condition(
        self,
        condition: Callable[[Self, Event], bool],
    ) -> None:
        """The next event satisfying a condition becomes activated.

        This function has no effect on schedule state if no events
        meet the condition.

        This function has no effect on schedule state if the next event
        meeting the condition is already active.
        """
        option_event = self.next_event_by_condition(condition)
        if option_event is not None:
            option_event.activate()

    def activate_all_events(self) -> None:
        """Activate all future events.

        Every event on the event queue will be activated.
        """
        self.apply_to_all_events(_activate_event)

    def activate_all_events_by_condition(
        self,
        condition: Callable[[Self, Event], bool],
    ) -> None:
        """Activate future events by condition.

        Every event that satisfies the given condition
        will be activated.
        """
        self.apply_to_events_by_condition(_activate_event, condition)

    def deactivate_next_event(self) -> None:
        """Deactive the next event in the event queue."""
        option_next_event = self.next_event()
        if option_next_event:
            option_next_event.deactivate()

    def deactivate_next_event_by_condition(
        self,
        condition: Callable[[Self, Event], bool],
    ) -> None:
        """Deactivate the next event that satisfies the given condition."""
        option_event = self.next_event_by_condition(condition)
        if option_event is not None:
            option_event.deactivate()

    def deactivate_all_events(self) -> None:
        """Deactivate all future events."""
        self.apply_to_all_events(_deactivate_event)

    def deactivate_all_events_by_condition(
        self,
        condition: Callable[[Self, Event], bool],
    ) -> None:
        """Deactivate future events by condition."""
        self.apply_to_events_by_condition(_deactivate_event, condition)

    def cancel_next_event(self) -> None:
        """Removes next event from the event schedule."""
        if self.event_queue:
            _ = heapq.heappop(self.event_queue)

    def cancel_next_event_by_condition(
        self,
        condition: Callable[[Self, Event], bool],
    ) -> None:
        """Cancel the next event that satisfies a given condition."""
        option_event = self.next_event_by_condition(condition)
        if option_event is not None:
            self.event_queue.remove((option_event.time, option_event))

    def cancel_all_events(self) -> None:
        """Removes all events from the event schedule."""
        self.event_queue = []

    def cancel_all_events_by_condition(
        self,
        condition: Callable[[Self, Event], bool],
    ) -> None:
        """Remove all events by a given condtion.

        Args:
        condition (Callable[[Self, Event], bool]): Callable that decides whether an event should be cancelled.

        """
        targets: list[Event] = []
        for _, event in self.event_queue:
            if condition(self, event):
                targets.append(event)
        for event in targets:
            self.event_queue.remove((event.time, event))

def _activate_event(event: Event) -> None:
    event.activate()


def _deactivate_event(event: Event) -> None:
    event.deactivate()

