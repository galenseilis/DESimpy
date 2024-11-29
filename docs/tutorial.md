# Tutorial

This tutorial goes through the fundamental components of DESimpy. There are two components of DESimpy that we will focus on: events and event schedulers. Once you know these components you will be ready to jump into building your own simulations or further studying from the topical guides.

## Events

In this section we're going to go through events in DESimpy.

### Creating Events

Events can be created explicitly. We will see later that we don't always have to make them explicit, but we should know that this is something that can do when needed.

Events only require being given the time that they should occur in a simulation. Below we initialize a single event.

```python
from desimpy import Event

example_event = Event(time=2018)
```

## Event Schedulers

Something has to orchestrate events unfolding over time. That's the job of `EventScheduler`, which we'll cover below.

### Creating Event Schedulers

You can initialize an event scheduler by calling it.

```python
from desimpy import EventScheduler

scheduler = EventScheduler()
```

Note that the event scheduler does not depend on anything initially. It is intended to be integrated with events, which we'll cover next.

### Event Schedulers Contain A Clock

Inside of every event scheduler is a clock that holds the current simulation time. You can access this time with the `EventScheduler.now` property like in the following example.

```python
from desimpy import EventScheduler

scheduler = EventScheduler()

print(scheduler.now)
```

Notice that the result of `scheduler.now` was zero. The simulation in a new event scheduler is always zero.

### Scheduling Events

Events on their own don't do much. If anything, they're just a glorified way to contain some data and delay a function call `Event.run`. It is their life cycle within an event scheduler that makes discrete event simulation come to life.

```python
from desimpy import Event, EventScheduler

TIME: float = 2018.0

event = Event(TIME)
scheduler = EventScheduler()

scheduler.schedule(event)
```

### Running A Simulation

We have now seen how to create and schedule events. Now it is time for us to create our first simulation. A common way to run a simulation is to call `EventScheduler.run_until_max_time` which will run the simulation until the specified time.

```python
from desimpy import Event, EventScheduler

event1 = Event(2018, lambda: print("It is 2018!"))
event2 = Event(2020, lambda: print("It is 2020!"))

scheduler = EventScheduler()
scheduler.schedule(event1)
scheduler.schedule(event2)

scheduler.run_until_max_time(2019)
```

Notice that only the `"It is 2018!"` is printed. That is because the simulation is going to stop at 2019, which is between 0 and 2020, but not continue on to 2020.

### Timeouts

While it isn't bad to define an event explicitly and then schedule it, we can save ourselves a little bit of effort by using the `EventScheduler.timeout` method.

```python
from desimpy import EventScheduler

scheduler = EventScheduler()

scheduler.timeout(2018)
```

There is an important difference between using `schedule` and `timeout`. The `schedule` method will take an event with the time that you want the event to elapse. The `timeout` method will schedule an event that is *delayed* by the amount of time that you specified. The former is a point in time whereas the latter is a duration following the current time. These two situations look identical when the simulation has not started, but we can now run a simulation to show the difference.

```python
from desimpy import Event, EventScheduler


```
