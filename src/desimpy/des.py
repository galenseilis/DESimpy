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

    def __init__(
        self, time: float, action: Callable = None, context: dict = None
    ) -> NoReturn:
        self.time = time
        self.action = (lambda: None) if action is None else action
        self.context = {} if context is None else context
        self.active = True

    def activate(self) -> NoReturn:
        """Activate event."""
        self.active = True

    def deactivate(self) -> NoReturn:
        """Deactivate event."""
        self.active = False

    def run(self):
        """Apply event's state transitions.

        The state transition will only occur if the
        event is active, in which case it will return
        whatever the event's action returns.

        If the event is inactive then the event's
        action will not occur, in which case `None`
        is implicitly returned by `run`.
        """
        if self.active:
            return self.action()

    def __le__(self, other):
        return self.time <= other.time

    def __lt__(self, other):
        return self.time < other.time


class EventScheduler:
    """Run discrete event simulations."""

    def __init__(self) -> NoReturn:
        self.current_time = 0
        self.event_queue = []
        self.event_log = []


    def next_event(self):
        """Refer to next event without changing it.

        This is sometimes called "peeking".
        """
        return heapq.nsmallest(1, self.event_queue)[0][1]

    def peek(self):
        """Get the time of the next event.

        Returns infinity if there is no next event.
        """
        next_event = self.next_event()
        if next_event:
            return next_event.time

        return float('inf')

    def schedule(self, event) -> NoReturn:
        """Schedule an event on the event queue.

        It is possible to schedule events with negative times
        provided that the current time is zero. In other words,
        before any time has elapsed it is permitted to schedule
        events that occur 'before' t=0. This may be referred to
        as "prescheduling". Sufficient care must be taken by the
        user to ensure that the desired behaviour is achieved with
        prescheduling.
        """
        if event.time >= 0 or self.current_time == 0:
            heapq.heappush(self.event_queue, (event.time, event))
        else:
            raise ValueError(f"{event.time=} must be non-negative.")

    def timeout(self, delay, action=None, context=None):
        """Schedule an event some delay into the future.

        This event is a convenience function around
        `self.schedule` that assumes the scheduled event
        occurs at some delay from the moment it is scheduled.
        """
        self.schedule(Event(self.current_time + delay, action=action, context=context))

    def activate_next_event(self):
        """Activate the next scheduled event."""
        self.next_event().activate()

    def activate_next_event_by_condition(self, condition: Callable):
        for event in self.event_queue:
            if condition(self, event):
                event.activate()
                break

    def activate_all_events(self):
        """Activate all future events.

        Every event on the event queue will be activated.
        """
        for event in self.event_queue:
            event.activate()

    def activate_all_events_by_condition(self, condition: Callable):
        """Activate future events by condition.

        Every event that satisfies the given condition
        will be activated.
        """
        for event in self.event_queue:
            if condition(self, event):
                event.activate()

    def deactivate_next_event(self):
        """Deactive the next event in the event queue."""
        self.next_event().deactivate()

    def deactivate_next_event_by_condition(self, condition: Callable):
        """Deactivate the next event that satisfies the given condition."""
        for event_pair in self.event_queue:
            if condition(self, event_pair):
                event_pair[1].deactivate()
                break

    def deactivate_all_events(self):
        """Deactivate all future events."""
        for event in self.event_queue:
            event.deactivate()

    def deactivate_all_events_by_condition(self, condition: Callable):
        """Deactivate future events by condition."""
        for event in self.event_queue:
            if condition(self, event):
                event.deactivate()

    def cancel_next_event(self) -> None:
        """Removes next event from the event schedule."""
        heapq.heappop(self.event_queue)

    def cancel_next_event_by_condition(self, condition: Callable):
        """Cancel the next event that satisfies a given condition."""
        for event in self.event_queue:
            if condition(self, event):
                target = event
                break
        if target is not None:
            self.event_queue.remove(event)

    def cancel_all_events(self) -> None:
        """Removes all events from the event schedule."""
        self.event_queue = []

    def cancel_all_events_by_condition(self, condition: Callable):
        """Remove all events by a given condtion."""
        targets = []
        for event in self.event_queue:
            if condition(self, event):
                targets.append(event)
        for event in targets:
            self.event_queue.remove(event)

    def _always_log_filter(self, event, event_result):
        """Keep all events in the event log."""
        return True

    def run(self, stop: Callable, log_filter: Callable = None, logging=True) -> list:
        """Run the discrete event simulation.

        By default every event will be logged, but for some simulations that may
        become an excessive number of events. Storing a large number of events in
        memory that are not of interest can be a waste of computer memory. Thus the
        `log_filter` function provides a way of filtering which events are logged.
        The `log_filter` expects an event, and keeps that event depending on the
        event itself (e.g. checking what is in context) as well as the result of the
        event (i.e. `event_result`).
        """
        if not logging:
            return self._run_without_logging(stop)
        elif log_filter is None:
            return self._run_always_logging(stop)
        else:
            return self._run_filtered_logging(stop, log_filter)

    def step(self):
        time, event = heapq.heappop(self.event_queue)
        self.current_time = time
        event_result = event.run()
        return event, event_result

    def _run_without_logging(self, stop: Callable) -> list:
        while not stop(self):
            if not self.event_queue:
                break
            self.step()

    def _run_always_logging(self, stop: Callable) -> list:
        while not stop(self):
            if not self.event_queue:  # Always stop if there are no more events.
                break
            event, event_result = self.step()
            self.event_log.append((event, event_result))
        return self.event_log

    def _run_filtered_logging(self, stop: Callable, log_filter: Callable):
        while not stop(self):
            if not self.event_queue:  # Always stop if there are no more events.
                break
            event, event_result = self.step()
            if log_filter(event, event_result):
                self.event_log.append((event, event_result))
        return self.event_log

    def run_until_max_time(
        self, max_time: float, log_filter: Callable = None, logging=True
    ):
        """Simulate until a maximum time is reached.

        This method is a convenience wrapper around the run
        method so that simulating until a maximum is assumed
        as the stop condition.
        """
        stop = lambda scheduler: (
                scheduler.current_time >= max_time
                or not scheduler.event_queue
                or heapq.nsmallest(1, scheduler.event_queue)[0][0] >= max_time
            )
        return self.run(stop, log_filter, logging)

    def run_until_event(self, event: Event, log_filter: Callable = None, logging=True):
        """Simulate until a given event has elapsed.

        This function is a convenience wrapper around the run
        method so that simulating until an event is elapsed is
        assumed as the stop condition."""
        stop = lambda scheduler: (
                event in scheduler.event_log
            )

        return self.run(stop, log_filter, logging)

