from enum import StrEnum, auto
from collections.abc import Callable, Hashable
from typing import Self

from _typing import ActionType

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
        self,
        time: float,
        action: Callable[[], object] | None = None,
        context: dict[Hashable, object] | None = None,
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
        self.action: Callable[[], object] = (lambda: None) if action is None else action
        self.context: dict[Hashable, object] = {} if context is None else context
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
            self.result: object = self.action()

    def __le__(self, other: Self):
        """Evaluate if this event is less-than-or-equal to another in time."""
        return self.time <= other.time

    def __lt__(self, other: Self):
        """Evaluate if this event is less than another in time."""
        return self.time < other.time


