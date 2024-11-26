"""```yaml
source: https://gitlab.com/team-simpy/simpy/-/issues/168
```
"""

raise NotImplementedError()

from desimpy import Event, EventScheduler


class School:
    """A school environment where pupils wait for the class to end (signaled by the bell)."""

    def __init__(self, env: EventScheduler) -> None:
        self.env = env
        self.bell_count = 0  # Count of bell rings
        self.pupil_responses = 0  # Count of pupil responses
        self.class_ended = False  # Flag to indicate class status

        # Create pupil processes (equivalent to SimPy processes)
        self.pupil_procs = [
            self.env.schedule(Event(self.env.current_time, lambda i=i: self.pupil(i)))
            for i in range(3)
        ]

        # Schedule the bell process
        self.bell_proc = self.env.schedule(Event(self.env.current_time, self.bell))

    def bell(self) -> None:
        """Simulate the bell ringing and end of class."""
        for _ in range(2):
            # Schedule the bell to ring after 1 time unit
            self.env.schedule(Event(self.env.current_time + 1, self.trigger_bell))

    def trigger_bell(self) -> None:
        """Trigger class end event."""
        print("Bell rings!")
        self.bell_count += 1  # Increment the bell count

        # Mark the class as ended
        self.class_ended = True

    def pupil(self, pupil_id: int) -> None:
        """Simulate a pupil responding to the bell."""
        for _ in range(2):
            print(
                f"Pupil {pupil_id}: Waiting for the class to end at time {self.env.current_time}"
            )

            # Wait until the class has ended (when bell rings)
            while not self.class_ended:
                yield self.env.schedule(
                    Event(self.env.current_time + 0.1, lambda: None)
                )  # Small delay

            print(
                f"Pupil {pupil_id}: Class ended, responding at time {self.env.current_time}"
            )
            self.pupil_responses += 1  # Increment the pupil response count
            self.class_ended = False  # Reset class status for the next bell


if __name__ == "__main__":
    # Example setup for the environment and school simulation
    env = EventScheduler()

    # Create the school with pupils and the bell process
    school = School(env)

    # Define a stopping condition function based on bell and pupil responses
    def stop_condition(scheduler: EventScheduler) -> bool:
        # Stop when both bell rings and pupil responses are complete
        return school.bell_count >= 2 and school.pupil_responses >= 6

    # Run the simulation until the defined stop condition is met
    env.run(stop=stop_condition)
