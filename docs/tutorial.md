# Tutorials

This tutorial goes through the fundamental components of DESimpy. There are two components of DESimpy that we will focus on.

## Events

### Creating Events

Events can be created explicitly. We will see later that we don't always have to make them explicit, but we should know that this is something that can do when needed.

```python
from desimpy import Event

example_event = Event()
```

## Event Schedulers

### Scheduling Events

```python
from desimpy import Event, EventScheduler

TIME: float = 2018.0

event = Event(TIME)
scheduler = EventScheduler()

scheduler.schedule(event)
```
