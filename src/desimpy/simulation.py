from enum import StrEnum, auto

from scheduler import EventScheduler


class SimulationStatus(StrEnum):
    """The status of an event scheduler."""

    INACTIVE = auto()
    ACTIVE = auto()


class Simulation:

    def __init__(self, scheduler: EventScheduler | None = None):
        """Initialize a simulation.

        Args:
            scheduler (EventScheduler): A user-defined event scheduler.
        """
        if scheduler is None:
            self.scheduler = EventScheduler()
        elif not isinstance(scheduler, EventScheduler):
            raise ValueError("Parameter `scheduler` must be an instance of `EventScheduler`")
        else:
            self.scheduler = scheduler

        self.current_time: float | int = 0
        self.status: SimulationStatus = SimulationStatus.INACTIVE

    @property
    def now(self) -> float:
        """Return current time.

        This property method concisely provides the
        current time in the simulation.
        """
        return self.current_time

    def _activate(self) -> None:
        """Set the simulation status to "active"."""
        self.status: SimulationStatus= SimulationStatus.ACTIVE

    def _deactivate(self) -> None:
        """Set the simulation status to "inactive"."""
        self.status: SimulationStatus = SimulationStatus.INACTIVE

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

        Running this function will activate, and subsequently deactivate, the simulation
        according to a binary variable, `Simulation.status`. This attribute will ensure
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
        event_time, event = heapq.heappop(self.scheduler.event_queue)
        self.current_time = event_time
        event.run()
        return event

    def _run_without_logging(self, stop: Callable[[Self], bool]) -> list[Event]:
        self._activate()
        while not stop(self):
            if not self.scheduler.event_queue:  # Always stop if there are no more events.
                break
            _ = self.step()
        self._deactivate()
        return self.scheduler.event_log

    def _run_always_logging(self, stop: Callable[[Self], bool]) -> list[Event]:
        self._activate()
        while not stop(self):
            if not self.scheduler.event_queue:  # Always stop if there are no more events.
                break
            event = self.step()
            self.scheduler.event_log.append(event)
        self._deactivate()
        return self.scheduler.event_log

    def _run_filtered_logging(
        self,
        stop: Callable[[Self], bool],
        log_filter: Callable[[Event], bool],
    ) -> list[Event]:
        self._activate()
        while not stop(self):
            if not self.scheduler.event_queue:  # Always stop if there are no more events.
                break
            event = self.step()
            if log_filter(event):
                self.scheduler.event_log.append(event)
        self._deactivate()
        return self.scheduler.event_log

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

        def stop_at_max_time(simulation: Simulation) -> bool:
            return (
                simulation.current_time >= max_time
                or not simulation.scheduler.event_queue
                or heapq.nsmallest(1, simulation.scheduler.event_queue)[0][0] >= max_time
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

        def stop_at_target_event(simulation: Simulation) -> bool:
            return event in simulation.scheduler.event_log

        return self.run(stop_at_target_event, logging)
