"""```yaml
description: Simulate a driver process interrupting a car charging process.
source: https://simpy.readthedocs.io/en/latest/simpy_intro/process_interaction.html#interrupting-another-process
contents:
    - 0. Imports.
    - 1. Define Car Class.
    - 2. Define Driver Process.
    - 3. Initialize Event Scheduler.
    - 4. Register Processes.
    - 5. Run Simulation.
```
"""

##############
# $0 IMPORTS #
##############

from desimpy import Event, EventScheduler

#######################
# $1 DEFINE CAR CLASS #
#######################


class Car:
    def __init__(self, env: EventScheduler) -> None:
        self.env: EventScheduler = env
        # Start the run process when an instance is created
        self.schedule_run()

    def schedule_run(self) -> None:
        """Schedule the initial run event."""
        self.env.timeout(0, self.schedule_charge)

    def schedule_drive(self) -> None:
        # Define the action to be executed when charging ends
        print(f"Start driving at {self.env.current_time}")

        # Schedule the next parking and charging event
        self.env.timeout(2, self.schedule_charge)

    def schedule_charge(self) -> None:
        """Handle the parking and charging, followed by driving."""
        print(f"Start parking and charging at {self.env.current_time}")

        # Schedule the charge process
        self.env.timeout(5, self.schedule_drive, context={"event_type": "charge"})


############################
# $2 DEFINE DRIVER PROCESS #
############################


def deactivate_next_charge_condition(env: EventScheduler, event: Event) -> bool:
    """Deactivate the charging event."""
    _ = env
    if event.context.get("event_type", None) == "charge":
        return True
    return False


def driver(env: EventScheduler, car: Car) -> None:
    def interrupt_action():
        print("Was interrupted. Hope, the battery is full enough ...")
        env.deactivate_next_event_by_condition(
            condition=deactivate_next_charge_condition
        )
        event = Event(env.current_time, car.schedule_drive)
        env.schedule(event)

    env.timeout(3, interrupt_action)


if __name__ == "__main__":
    #################################
    # $3 INITIALIZE EVENT SCHEDULER #
    #################################

    scheduler = EventScheduler()

    #########################
    # $4 REGISTER PROCESSES #
    #########################

    car = Car(scheduler)
    driver(scheduler, car)

    #####################
    # $5 RUN SIMULATION #
    #####################

    _ = scheduler.run_until_max_time(15, logging=False)
