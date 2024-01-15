# DESimPy
Event-driven [discrete event simulation](https://en.wikipedia.org/wiki/Discrete-event_simulation) in Python (DESimPy).

## Overview

DESimPy is an event-driven simulation framework based on standard Python and inspired by [SimPy](https://simpy.readthedocs.io/en/latest/).

Processes in DESimPy are defined by methods owned by Python objects inherited from the `Event` abstract base class. These processes can be used to model system-level or component level changes in a modelled system. Such systems might include customers or patients flowing through services, vehicles in traffic, or agents competing in games.

DESimPy implements time-to-event simulation where the next event in a schedule is processed next regardless of the amount of time in the simulated present to that event. This constrasts with "time sweeping" in which a step size is used to increment foreward in time. It is possible to combine time-to-event with time sweeping (see [Palmer & Tian 2021](https://www.semanticscholar.org/paper/Implementing-hybrid-simulations-that-integrate-in-Palmer-Tian/bea73e8d6c828e15290bc4f01c8dd1a4347c46d0)), however this package does not provide any explicit support for that.


Here is the [clock example](https://simpy.readthedocs.io/en/latest/) from the SimPy package (an inspiration for this package) implemented in DESimPy.

The clock example highlights two important differences between SimPy and DESimPy. The first is that in DESimPy events are responsible for processes whereas in SimPy events are not (but are coupled to events). In DESimPy events occur only at points in time, so the notion of a process which has a beginning time and and ending time is implemented by two events in which the first event triggers.

DESimPy is released under a GNU GPL license.


## Quickstart

In this section you'll learn the basics of DESimPy that will allow you to start developing your own event-driven discrete event simulations.
