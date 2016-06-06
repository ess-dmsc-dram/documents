## Plankton Architecture

This section covers how Plankton is organized, and design decisions made during development.


### Cycle-based Simulation

The simulation operates based on process cycles with a Delta T parameter. 

The internal state of the simulation will only change during a cycle.

Outside of a cycle, the user may query the current state and set properties that will take effect next cycle.

This has the following advantages:

- Can act "autonomously" rather than just reacting
- Predictable, deterministic behaviour
- Speed may modulated by adjusting Delta T between cycles
- Resolution may be modulated by adjusting cycles per second


### Cycle-based StateMachine

StateMachine had to be cycle-based as well, so we created our own implementation.

Once set up, will raise cycle events as needed during a process cycle. There are three kinds of events:

- on_entry
- in_state
- on_exit

All events receive a Delta T and are expected to behave accordingly.

A single cycle will:

- May perform at most one transition (if conditions satisfied)
- May exit current state and enter new state (if a transition occurred)
- Will perform exactly one in_state event as the last step of the cycle


### Context

The concept of a device context was introduced to be able to track and share the device "state".

Essentially a struct that contains inputs, outputs, and internal variables. 

Can be thought of as the device's memory, as opposed to StateMachine state.

Is provided as `self._context` to classes that inherit `HasContext`.


### Device

Devices represent a physical device and implement its baseline behaviour by configuring a StateMachine and providing default state implementations.

Devices are located in the `plankton/devices` folder as subfolders. 

They should contain at least a `device.py`, which sets up the StateMachine and provides a Context, and a `defaults.py`, which defines the default states and their behaviour.


### Setup

Setups are a particular configuration of a device, and potentially provide it with modified behaviour by overriding States.

Setups are located in the `plankton/setups` folders as subfolders, mirroring the `plankton/devices` folder.

Each file inside represents one setup. The setup defined in `default.py` is loaded by default, when a user starts a device simulation without specifying a setup.

`bindings.py` is a special file that is currently used to "connect" the device to its adapter.


### Adapter

An adapter is used to expose a device, with its applied setup, over a particular protocol.

Currently only an EPICS adapter is available.

Ideally, we want a single adapter per protocol that works with any device and, conversely, for any given device to work with any protocol. However, some "glue" is required... which the `bindings.py` file currently provides.

This part of Plankton is still very prototypal and will likely change dramatically as development continues.
