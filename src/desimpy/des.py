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

    def schedule(self, event) -> NoReturn:
        """Schedule an event on the event queue."""
        heapq.heappush(self.event_queue, (event.time, event))

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

    def activate_all_events(self):
        """Activate all future events."""
        for event in self.event_queue:
            event.activate()

    def activate_all_events_by_condition(self, condition: Callable):
        """Activate future events by condition."""
        for event in self.event_queue:
            if condition(self, event):
                event.activate()

    def deactivate_next_event(self):
        """Deactive next event."""
        self.next_event().deactivate()

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

    def cancel_all_events(self) -> None:
        """Removes all events from the event schedule."""
        self.event_queue = []

    def interrupt_next_event(self, method="deactivate", next_event=None):
        """Interrupt the next event in the schedule.

        Events can be interrupted via two distinct methods which pertain to how the
        interrupted event is handled. The first, and default, method is to deactivate 
        the interrupted event. This means that its `run` method will not run. The second
        method is to cancel the event, which is to remove the event from the event schedule
        altogether.

        Events can either be interrupted with or without another event being placed on the event
        schedule.
        """
        next_time = next_event.time if next_event is not None else self.current_time
        next_event = next_event or heapq.nsmallest(2, self.event_queue)[-1][1]
        if method == "deactivate":
            self.deactivate_next_event()
        elif method == "cancel":
            self.cancel_next_event()
        else:
            raise NotImplementedError(
                f"{method=} is not implemented for interrupt_next_event."
            )

        next_event.time = next_time
        self.schedule(next_event)

    def interrupt_next_event_by_condition(self, condition: Callable, method='deactivate', next_event=None):
        """Interrupt the next event that satisfies a given condition."""
        next_time = next_event.time if next_event is not None else self.current_time
        queue_snapshot = heapq.nsmallest(len(self.event_queue), self.event_queue)
      
        # Search for an event to interrupt.
        interrupted_event = None
        for idx, event in enumerate(queue_snapshot):
            if condition(self, event):
                interrupted_event = event
                next_event = next_event or heapq.nsmallest(idx + 2, self.event_queue)[-1][1]
                break

        # If an event could not be interrupted, then go no further.
        if interrupted_event is None:
            return

        # Handle the interrupted event.
        if method == 'deactivate':
            interrupted_event.deactivate()
        elif method == 'cancel':
            queue_snapshot.pop(idx)
            self.cancel_all_events()
            for event in queue_snapshot:
                self.schedule(event)
        else:
            raise NotImplementedError(
                f"{method=} is not implemented for interrupt_next_event_by_condition."
            )

        # Schedule the next event
        next_event.time = next_time
        self.schedule(next_event)

    def _always_log_filter(self, event, event_result):
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

        log_filter = (lambda event, event_result: True) if log_filter is None else log_filter
        while not stop(self):
            if not self.event_queue:  # Always stop if there are no more events.
                break
            time, event = heapq.heappop(self.event_queue)
            self.current_time = time
            event_result = event.run()
            if log_filter(event, event_result):
                self.event_log.append((event, event_result))
        return self.event_log

    def run_until_max_time(self, max_time: float, log_filter: Callable = None):
        """Simulate until a maximum time is reached.

        This method is a convenience wrapper around the run
        method so that simulating until a maximum is assumed
        as the stop condition.
        """
        return self.run(_stop_at_max_time_factory(max_time), log_filter)


def _stop_at_max_time_factory(max_time: float) -> Callable:
    """Stop function to halt the simulation at a maximum time.

    Define the scheduler first, then call this function on it
    with the desired max_time to get the desired function. Finally,
    call the event scheduler's run method on the function.
    """
    return lambda scheduler: (
        scheduler.current_time >= max_time
        or not scheduler.event_queue
        or heapq.nsmallest(1, scheduler.event_queue)[0][0] >= max_time
    )
