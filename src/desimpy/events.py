from typing import NoReturn

from desimpy import core

class TimeoutEvent(core.Event):
    """An event that times out another given event after a specified timeout."""

    def __init__(
        self,
        env: core.Environment,
        time: float,
        target_event: core.Event,
        timeout: float,
        execute: bool = False,
    ) -> NoReturn:
        """
        Args:
            env (Environment): Simulation environment instance.
            time (float): Scheduled time of timeout.
            target_event (Event): Event to be timed out.
            timeout (float): Amount of time until target event is timed out.
            execute (bool): Whether to execute the event when it times out.
        """
        super().__init__(env, time)
        self.target_event = target_event
        self.timeout = timeout
        self.execute = execute

    def execute(self) -> NoReturn:
        """Execute the timeout event."""

        if not self.target_event.elapsed:
            self.target_event.elapsed = True  # Mark the target event as elapsed

            if self.execute:
                self.target_event.execute()  # Execute the target event immediately


class DelayNextEvent(core.Event):
    """Event that delays the next event in the schedule."""

    def __init__(self, env: core.Environment, time: float, delay: float) -> NoReturn:
        '''Initialize event that delays another event.'''
        super().__init__(env, time)
        self.delay = delay

    def execute(self) -> NoReturn:
        '''Delay the next event if there is one.'''
        if self.env.event_queue:
            next_time, next_event = heapq.heappop(self.env.event_queue)
            new_time = next_time + self.delay
            next_event.time = new_time
            self.env.schedule_event(next_event, new_time)

class DelayAllEvent(core.Event):
    '''Delay all events on the event schedule.'''

    def __init__(self, env: core.Environment, time: float, delay: float) -> NoReturn:
        super().__init__(env, time)
        self.delay = delay

    def execute(self):
        '''Delay all scheduled events.'''
        new_schedule = []
        for (event_time, event) in self.env.event_queue:
            new_time = event_time + self.delay
            event.time = new_time
            new_schedule.append((new_time, event))
        self.env.event_queue = new_schedule
