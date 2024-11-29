# Explanation


## Theory

Discrete event simulation (DES) can be understood through different concepts and formalisms.

### Foo

DES can be informally broken into a few components:

- state: A set of variables representing the way that a system is at some point in time.
- clock: A variable which keeps track of the simulation time.
- event list: The sequence of events that have yet to have elapsed in the simulation.
- random-number generators: instructions to generate pseudorandom numbers.
- statistics:
- end condition: the contexts in which the simulation should stop.
- three-phase approach

### DEVS

Coming soon...

## Design

DESimpy was made with certain goals and non-goals in mind. It isn't meant to be everything, and it isn't meant to be nothing. It is meant to give a starting point for a certain audience of computer programmers.

### Goals

- Provide minimal components for handling times and schedules.
    - Keep it simple.
- Provide a built-in, but optional, event logging system.
- Follow [Diátaxis framework](https://www.diataxis.fr/) in developing and maintaining this documentation.

### Non-Goals

- Provide batteries-included discrete event simulation tools. DESimpy provides the bricks; you must imagine cathedrals.
- Use coroutines to improve readability or provide asychronous input/output with data sources.
- Provide pseudorandom number generators.
- Have events be scheduled in any order other than the time that they elapse.
- Implementing real-time simulations.
