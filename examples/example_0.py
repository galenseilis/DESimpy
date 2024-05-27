from desimpy import core

class CustomEvent(core.Event):
    """Custom event for demonstration."""

    def execute(self, env) -> None:
        """Execution logic of the custom event."""
        print(f"Custom event executed at time {env.now}")

class Simulation:
    """Simple simulation example."""

    def __init__(self) -> None:
        """Initialize the simulation environment."""
        self.env = core.Environment()

    def run_simulation(self) -> None:
        """Run the simulation."""
        event = CustomEvent(5)  # Schedule the custom event at time 5
        self.env.schedule_event(event)
        self.env.run(10)  # Run the simulation for 10 time units

if __name__ == "__main__":
    sim = Simulation()
    sim.run_simulation()

