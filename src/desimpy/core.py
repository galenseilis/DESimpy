"""Core components of a discrete event simulation (DES)."""

# /$$$$$$$  /$$$$$$$$  /$$$$$$  /$$               /$$$$$$$
# | $$__  $$| $$_____/ /$$__  $$|__/              | $$__  $$
# | $$  \ $$| $$      | $$  \__/ /$$ /$$$$$$/$$$$ | $$  \ $$ /$$   /$$
# | $$  | $$| $$$$$   |  $$$$$$ | $$| $$_  $$_  $$| $$$$$$$/| $$  | $$
# | $$  | $$| $$__/    \____  $$| $$| $$ \ $$ \ $$| $$____/ | $$  | $$
# | $$  | $$| $$       /$$  \ $$| $$| $$ | $$ | $$| $$      | $$  | $$
# | $$$$$$$/| $$$$$$$$|  $$$$$$/| $$| $$ | $$ | $$| $$      |  $$$$$$$
# |_______/ |________/ \______/ |__/|__/ |__/ |__/|__/       \____  $$
#                                                           /$$  | $$
#                                                          |  $$$$$$/
#                                                           \______/

###########
# IMPORTS #
###########

from __future__ import annotations

import heapq  # pragma: nocover
from enum import StrEnum, auto
from typing import TYPE_CHECKING, final  # pragma: nocover

if TYPE_CHECKING:
    from collections.abc import Callable
    from typing import Any, Self

#################
# CONFIGURATION #
#################

__all__ = ["Event", "Environment"]  # pragma: nocover

####################
# EVENT DEFINITION #
####################


class EventStatus(StrEnum):
    """The status of an event."""

    INACTIVE = auto()
    ACTIVE = auto()


class Event:
    """DES event.

    Represents a state transition that can be scheduled by the event scheduler.

    The context variable is to provide information for two purposes.

    The first is provides a general way for events to store "properties" that are
    specific to the simulation without the implementation of the DES components
    being strongly coupled to them. That facilities events being part of control
    flow in other parts of the simulation while also being relatively isolated.

    The second purpose for `context` is logging information that was true at the
    time that the event was defined. This will often, although not always, be the
    same simulation time as when the event was scheduled.

    The output of `action` is also for logging purposes. It should not be used
    for control flow within the system specific details of the simulation, and
    its role in the core discrete event simulation implementation is to provide
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

    def __init__(
        self,
        time: float,
        action: Callable[[], Any] | None = None,
        context: dict[Any, Any] | None = None,
    ) -> None:
        """Create instance of an event."""
        # OPTIMIZE: Validation checks that are removed when run in optimized mode.
        if __debug__:
            # INFO: The checks below are considered unreachable by PyRight,
            # but they are.
            if not isinstance(time, int | float):
                raise TypeError(f"{time=} must be a number.")
            if not (isinstance(context, dict) or context is None):
                raise TypeError(f"{context=} must be a dictionary or None.")
            if not (callable(action) or action is None):
                raise TypeError(f"{action=} must be a callable or None.")

        self.time: float | int = time
        self.action: Callable[[], Any] = (lambda: None) if action is None else action
        self.context: dict[Any, Any] = {} if context is None else context
        self.status: EventStatus = EventStatus.ACTIVE
        self.result = None

    def activate(self) -> None:
        """Activate event."""
        self.status = EventStatus.ACTIVE

    def deactivate(self) -> None:
        """Deactivate event."""
        self.status = EventStatus.INACTIVE

    def run(self) -> None:
        """Apply event's state transitions.

        The state transition will only occur if the
        event is active, in which case it will return
        whatever the event's action returns.

        If the event is inactive then the event's
        action will not occur, in which case `None`
        is implicitly returned by `run`.
        """
        if self.status == EventStatus.ACTIVE:
            self.result: Any = self.action()

    def __le__(self, other: Self):
        """Evaluate if this event is less-than-or-equal to another in time."""
        return self.time <= other.time

    def __lt__(self, other: Self):
        """Evaluate if this event is less than another in time."""
        return self.time < other.time


#####################################
# SIMULATION ENVIRONMENT DEFINITION #
#####################################


class EnvironmentStatus(StrEnum):
    """The status of an event scheduler."""

    INACTIVE = auto()
    ACTIVE = auto()


class Environment:
    """Discrete event simulation run environment."""

    def __init__(self) -> None:
        """Create an event scheduler."""
        self.current_time: float | int = 0
        self.event_queue: list[tuple[float, Event]] = []
        self.event_log: list[Event] = []
        self.status: EnvironmentStatus = EnvironmentStatus.INACTIVE

    @property
    def now(self) -> float:
        """Return current time.

        This property method concisely provides the
        current time in the simulation.
        """
        return self.current_time

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
                raise TypeError(
                    f"{event=} must be of type {Event.__qualname__} but got {type(Event)=}."
                )
            if not (event.time >= 0 or not self.status == EnvironmentStatus.ACTIVE):
                raise ValueError(
                    f"{event.time=} must be non-negative once simulation has become active.",
                )

        heapq.heappush(self.event_queue, (event.time, event))

    def timeout(
        self,
        delay: float,
        action: Callable[[], Any] | None = None,
        context: dict[Any, Any] | None = None,
    ) -> None:
        """Schedule an event some delay into the future.

        This event is a convenience function around
        `self.schedule` that assumes the scheduled event
        occurs at some delay from the moment it is scheduled.
        """
        event = Event(self.current_time + delay, action=action, context=context)
        self.schedule(event)

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

    def apply_to_all_events(self, func: Callable[[Event], Any]) -> None:
        """Apply a function to all events in schedule."""
        for _, event in self.event_queue:
            func(event)

    def apply_to_events_by_condition(
        self,
        func: Callable[[Event], Any],
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
        """Deactivate the next event in the event queue."""
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
        """Remove all events by a given condition.

        Args:
        condition (Callable[[Self, Event], bool]): Callable that decides whether an event should be cancelled.

        """
        targets: list[Event] = []
        for _, event in self.event_queue:
            if condition(self, event):
                targets.append(event)
        for event in targets:
            self.event_queue.remove((event.time, event))

    def run(
        self,
        stop: Callable[[Self], bool],
        logging: Callable[[Any], bool] | bool = True,
    ) -> list[Event]:
        """Run the discrete event simulation.

        By default every event will be logged, but for some simulations that may
        become an excessive number of events. Storing a large number of events in
        memory that are not of interest can be a waste of computer memory. Thus the
        `log_filter` function provides a way of filtering which events are logged.
        The `log_filter` expects an event, and keeps that event depending on the
        event itself (e.g. checking what is in context) as well as the result of the
        event (i.e. `event_result`).

        Running this function will activate, and subsequently deactivate, a the simulation
        according to a binary variable, `Environment.status`. This attribute will ensure
        consistent scheduling of variables in temporal order during simulations provided
        that Python's `__debug__ == True`.
        """
        # OPTIMIZE: Chooses efficient implementation.
        if not logging:
            return self._run_without_logging(stop)
        if callable(logging):
            return self._run_filtered_logging(stop, logging)
        return self._run_always_logging(stop)

    def step(self) -> Event:
        """Step the simulation forward one event."""
        event_time, event = heapq.heappop(self.event_queue)
        self.current_time = event_time
        event.run()
        return event

    def _run_without_logging(self, stop: Callable[[Self], bool]) -> list[Event]:
        self._activate()
        while not stop(self):
            if not self.event_queue:  # Always stop if there are no more events.
                break
            _ = self.step()
        self._deactivate()
        return self.event_log

    def _run_always_logging(self, stop: Callable[[Self], bool]) -> list[Event]:
        self._activate()
        while not stop(self):
            if not self.event_queue:  # Always stop if there are no more events.
                break
            event = self.step()
            self.event_log.append(event)
        self._deactivate()
        return self.event_log

    def _run_filtered_logging(
        self,
        stop: Callable[[Self], bool],
        log_filter: Callable[[Event], bool],
    ) -> list[Event]:
        self._activate()
        while not stop(self):
            if not self.event_queue:  # Always stop if there are no more events.
                break
            event = self.step()
            if log_filter(event):
                self.event_log.append(event)
        self._deactivate()
        return self.event_log

    def run_until_max_time(
        self,
        max_time: float,
        logging: Callable[[Self], bool] | bool = True,
    ) -> list[Event]:
        """Simulate until a maximum time is reached.

        This method is a convenience wrapper around the run
        method so that simulating until a maximum is assumed
        as the stop condition.
        """

        def stop_at_max_time(scheduler: Environment) -> bool:
            return (
                scheduler.current_time >= max_time
                or not scheduler.event_queue
                or heapq.nsmallest(1, scheduler.event_queue)[0][0] >= max_time
            )

        results = self.run(stop_at_max_time, logging)
        self.current_time = max_time
        return results

    def run_until_given_event(
        self,
        event: Event,
        logging: Callable[[Self], bool] | bool = True,
    ) -> list[Event]:
        """Simulate until a given event has elapsed.

        This function is a convenience wrapper around the run
        method so that simulating until an event is elapsed is
        assumed as the stop condition.
        """

        def stop_at_target_event(scheduler: Environment) -> bool:
            return event in scheduler.event_log

        return self.run(stop_at_target_event, logging)

    def _activate(self) -> None:
        """Set the simulation status to "active"."""
        self.status: EnvironmentStatus = EnvironmentStatus.ACTIVE

    def _deactivate(self) -> None:
        """Set the simulation status to "inactive"."""
        self.status: EnvironmentStatus = EnvironmentStatus.INACTIVE


######################
# HELPER DEFINITIONS #
######################


def _activate_event(event: Event) -> None:
    event.activate()


def _deactivate_event(event: Event) -> None:
    event.deactivate()
