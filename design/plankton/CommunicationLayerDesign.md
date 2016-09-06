# Plankton Communication Layer Design

## Motivation
Plankton has been successfully used to implement detailed device simulations using its cycle-driven, state-machine-based approach. However, while implementing the first few simulators, it has become clear that the communication layer is not flexible enough to support all desired use cases.

The purpose of this document is to evaluate design options to resolve this by explicitly listing all required and desired features, and detailing proposed solutions that will satisfy them. Once all parties have had a chance to contribute design proposals, all proposals will be evaluated and a recommended design will be accepted by friendly consensus.

## Requirements

### ESS Requirements
Requirements listed in this section are required by the ESS. Design proposals that don't satisfy all items cannot be accepted as the recommended design.

1. The system shall isolate the device simulation from protocol details
2. The system shall drive the cycle-based simulation independently from any protocol
3. The system shall support simulations at both the IOC level and the device level
4. The system shall support the following protocols: TCP Stream, Modbus, EPICS
5. The system shall be designed in a way that allows for further protocols
6. The system shall be able to simulate devices which provide their interface on multiple protocols
7. The system shall be able to simulate devices which split their interface across different protocols
8. The system shall support changing and retrieving simulation parameters at runtime via these protocols
9. The system shall allow customizing protocol error handling for each device
10. The system shall allow customizing protocol payload format for each device
11. The system shall have layers that can be independently tested

### External User Requirements
Requirements listed here are of interest if we want Plankton to be usable and attractive to third parties. 

The IBEX team at ISIS, for example, have expressed interest in using Plankton. Not all of these items have to be satisfied for Plankton to be useful to external users, but supporting as many as possible will likely make Plankton a much more attractive solution.

1. The system should minimize effort and burden of knowledge for users seeking to implement simulators
2. The system should allow for traceability between device specification and simulation implementation
3. The system should allow querying and tweaking device internals outside of normal device functionality
4. The system should clearly separate device supported behaviour and any additional debug behaviour
5. The system should be able to log simulation activity with minimal effort for simulation developers
6. The system should be able to track and report number of cycles processed and how much time passed

## Design Options

### Adapter-Binder Approach

Overview:

* `Adapters` are bespoke per `Device` as well as per `Protocol`.
* We term the `Hardware` as per the manufacturer specification to be `Device` + `Adapter`.
* There is no separate binding.
* There is no general concrete `Adapter` for any protocol. 
* The process loop is kicked off by the `Environment`

#### Adapters

The problem with the current implementation is that the `Adapter` concept is too general and the `Binder` mechanism is too limited (1:1) to make linkup to a `Device` powerful or flexible enough.

The `Adapters` in this design are per-protocol & per-device. So they can encapsulate all the logic necessary to drive the specific device that they wrap. 

```python
class StreamAdapterLinkum95(StreamAdapter):
    def __init__(self, linkum95_device):
        if not isinstance(linkum95, SimulatedLinkamT95):
            raise ValueError("StreamAdapterLinkum95 only wraps the SimulatedLinkamT95 device") 
        self._device = linkum95_device
            
class EPICSAdapterLinkum95(EPICSAdapter):
    def __init__(self, linkum95_device):
        if not isinstance(linkum95, SimulatedLinkamT95):
            raise ValueError("EPICSAdapterLinkum95 only wraps the SimulatedLinkamT95 device")
        self._device = linkum95_device                     
```

Adapters are device owners. In the context of the current `linkum95`, the binary flags which are critical to this device would be moved into the associated `StreamAdapterLinkum95`. The state-machine parts of the `Device` are therefore essentially free of the `Hardware` interface. See next section for new-users and external contributions and how we intend to make this separation optional.

#### The Device-Adapter Types

The system should address the needs of the instrument-data group as a priority. That is to implement robust simulators meeting testable and maintainable internal standards. For this device and adapter separation is vital. In this mode of operation the `Device` represents the state-machine independent of the `Adapter` and the `Adapter` turns the `Device` into the `Hardware-Device` which both behaves and communicates as per the real hardware as specified by the manufacturer. For internally developed devices we would expect to see **three factor testing**:

1. Testing of the state-machine `Device`
2. Testing of the `Adapter` with a mocked `Device`
3. Integration tests of the entire `Hardware` (`Device` + `Adapter`) against the hardware specifications.

However, we also have a requirement:

```
The system should minimize effort and burden of knowledge for users seeking to implement simulators
```

Users are likely to implement a device top-down. That is to say that they will start with the device specification, build the adapter an think about the state-machine from there. In this case, the separation of `Adapter` from `Device` becomes a burden and makes things harder for device implementors. The approach here is to provide support for a single combination class, which front facing documentation should heavily promote for new users:

```python
class SimulatedLinkum95Hardware(StreamAdapter, Device):
    pass
```
The plankton framework will handle registration of such devices. If users wanted to promote such devices to be distributed with the framework, they could request to do so and it should be possible for us to make the conversion. **We would only require that point 3 of the three factor testing (above) had been provided.**

#### Device and Low-Level Design and Testing

For example, The Linkum T95 returns a hexadecimal temperature status when probed via a TCP 'T'. That's what the data sheet says. That's unambiguous. **Any design must support this ability and we should test at this level**. We should treat testing at this level as *system-testing* or *integration-testing* of the device. For the remainder of this section I'll call this the `Adapter-Interface`. 

However, the specification does not specify that there is a state-machine. We use a state-machine to provide a good model of the device behaviour.  For the remainder of this section I'll call this my `State-Machine-Device` which would encompass the `Context` the `OrderedDict` state-machine specification along with transition functions.

Here is why I (Owen) think this split is important.

Premise: Fundamentally "TESTING IS THE PROCESS OF EXECUTING A PROGRAM WITH THE INTENT OF FINDING ERRORS" *G.J Myers, The Art of Software Testing, Wiley, 1979*

1. My state-machine realisation can be sufficiently complex that I want to test that independently from what the specified interface promises. This is white-box testing of my state-machine device. The chopper is quite complex, but Plankton is powerful enough to do state-based simulations of much greater complexity than the chopper, and we should make the framework suitable for that for our internal device creations.
1. The `Adapter-Interface` does not promise to provide sufficient hooks for me to test my internal implementation of my state machine. The interfaces are different. The device manufactures did not know that I intended to create a state machine simulator, and their interface is different to the one that I want for my state machine.
1. The `Adapter-Interface` interface includes conversions that are not fundamental to my state-machine and my state-machine does not rely on those conversions. For example, the `Adapter-Interface` returns a temperature as `32` degrees as `0x020`.
    1. I want to be able to verify that the device is processing say a temperature limit set `L1` to the correct temperature independently of what the `State-Machine-Device` then does with it. I want failures to easily indicate where problems are in the code base (see premise above). Are they related to the state-machine or the parsing of inputs?
    1. I want to have readable tests for my `State-Machine-Device` a set/return `0x020` is not incredibly readable at the unit test level (although it is needed at the system-test level)


#### Environment & Timing Loop

The design separates the timing loop from the `Adapter`. The while loop is built into an `Environment`, of which there is just one per simulation. We would like to be able to make updates to the `Environment` without having ot restart the simulation or renew the adapters. One possible implementation of the `Environment` might look like this:

```python

class Environment(object):

    def __init__(self, adapter):
        self._adapter = adapter # adapter wraps device (see above)
        self._count = 0
        self._timer = 0.0
        self._delta = 0.0
        self._user_delta = None
        
    def _delta(self):
        if self._user_delta:
            return self._user_delta
        else:
            return (datetime.now() - start).total_seconds()
            
    def set_user_delta(self, delta):
        self._user_delta = delta

    def run(self):

        while True:
            start = datetime.now()

            
            self._adapter.process(delta) # stream adapters would call asyncore.loop(0.1, count=1) as part of this

            
            count += 1
            timer += self._delta()
            self._delta = self._delta()
            # ....
```

#### Environment Updates

The separation of the runnable parts of the simulation (now in the `Environment`) from the `Device` and the `Adapter` parts should make updates which affect only the `Environment` easier.

Here's one possibility I've been considering:

`EnvironmentAdapter` sees `Environment` 

```python 
    class Environment(object):

    def __init__(self, adapter, environ_adapter):
        self._environ_adapter = environ_adapter
        self._environ_adapter.set_adaptee(self)
        self._adapter = adapter

    def run(self):

        while True:
            # Everything still driven from a central processing loop.
            self._environment_adapter.process()
            
            self._adapter.process(delta)

```

```python
   class StreamEnvironmentAdapter(object):

    def set_adaptee(self, environment):
        self._environment = environment
        
    
    def process(self):
        asyncore.loop(0.1, count=1)
        # ...
        self._environment.set_user_delta(user_value)
        
```

After discussion with Michael Wedel, I am now strongly leaning towards providing a simple single protocol for the `Environment Control`. While `Adapter` flexibility and variation is vital in order to support different device types. the `Environment` is internal to plankton and we should publish and control a single mechanism for this. Michael Wedel has suggested JSON over zeromq.

#### Author Comments

I believe this design will satisfy all the listed requirements. But I would be happy to answer questions against any one of the listed requirements and expand my design accordingly.

**Benefits**

* The `Adapter` is completely responsible for binding a device specific input protocol to the relevant device. Protocols are designed for devices, and this approach recognises that. 
* There is **no** separate binding layer. The bindings responsibility is part of the `Adapter` this allow for complex binding behaviour to be modelled.
* The Adapter can be tested independently of the `Device`. The `Device` can be mocked for these testing purposes.
* The `Device` is not aware of the `Adapter`. `Devices` can be tested independently of the `Adapter`
* The `Environment` can be updated on a running device.

**Drawbacks**

* The design lacks a good way to enforce that a given device-adapter class uses any shared-code.
* Can we implement `EnvironmentAdapters` to run on the same thread as the rest of the application? (I think the answer is probably yes). If not locking may become a problem.

#### New package structure

With the design explained above it becomes more straight forward to specify a package structure that is suitable for distribution (e.g. as a package in PyPI). What we could aim for is a package that has several modules:

* `core`: Contains the state machine and base classes for different adapters, as well as some behavior that is useful for devices (e.g. "approach a value" stuff discussed in [#81](https://github.com/DMSC-Instrument-Data/plankton/issues/81)). These could be in sub-modules/packages `statemachine`, `behavior`, `adapters`, `utilities`.
* `devices`: These would contain one sub-module per device, at the moment `chopper` and `linkam_t95`, which in turn contain the device implementation as well as the adapter(s) associated with that device. The setups should also be in a sub-module of the device.
* `devices_contrib` (maybe there is a better name?): This is where external developers would add their devices to begin with. As @owenarnold wrote above, later refactoring done by us (or experienced developers) would move the device into the `devices` package. There is no strict need to have an entire directory per device, it could be a single Python file to begin with.
* `simulation`: This would contain the current startup script and possibly a "server mode simulation runner" which is controllable via the protocol described above.
* `tests`: Tests for all the stuff above. Contributors would put their tests into `tests/devices_contrib`. This would probably not be part of the PyPI-package.

We could then think about providing a PyPI-package, where users can just do `pip install plankton` and use the core parts (statemachine etc.) for other stuff simply via `from plankton.core import statemachine` or `from plankton.devices import chopper` to write some device related script.

Furthermore the `setup.py`-file can be configured so that the startup script (both the current one and the potential new one for a daemon) are installed into the system's path.

The package building and publishing can probably be done via travis as well, but that needs to be verified.


#### Example Adapter Code

This section provides a code example that shows how this design might be implemented, tracing from adapter to device class.

In this code, terminology is as follows:
- Adapter: Base class that implements low level protocol handling and communication (TCP, EPICS, etc).
- Interface: A device's high level interface on a protocol, and maps it to python methods (`'T'` -> `getStatus()`). Inherits from Adapter.
- Device: Sets up device `StateMachine` and contains device attributes (formerly contained in Context).

```python
#############################################################
# plankton/adapters/stream.py
#------------------------------------------------------------

class StreamHandler(asynchat.async_chat):
    # Mostly same as currently in stream.py
    # Handles a specific tcp connect
    # Created by StreamServer
    # Calls StreamAdapter.handleCommand from self.found_terminator
    pass

class StreamServer(asyncore.dispatcher):
    # Same as currently in stream.py
    # Listens on port XYZ for incoming connections
    # Still created by StreamAdapter?
    pass

class StreamAdapter(Adapter):
    # Very different from current in stream.py
    # Main loop / run method moved to environment
    
    # All Adapters have a process, this one just gives asyncore some time to
    # handle its connections. Perhaps the only thing Adapters have in common?
    # NOTE: Parameter is not dt, but how long we should spend here at most.
    #       This is important now that we want to provide dt/cycle control.
    def process(self, how_long=0.1):
        # Could add some code to ensure we spend a full how_long worth of time
        # here (rather than returning early if a connection is handled).
        asyncore.loop(how_long, count=1)
    
    # Register command handlers, called by decorators below
    def registerCommand(self, func, regex):
        # Add regex -> func mapping to some internal dict or the like
        pass
    
    # Called by StreamHandler when new command arrives
    def handleCommand(self, command):
        # Match command against internal dict of regex -> func
        # Call func (arg contents/number depend on regex capture groups)
        # return back to StreamHandler (which sends return value over wire)
        return func(*args)  # calls, e.g.: setRate('2000')
        
    # @stream_command and @stream_default_command decorators defined here?


#############################################################
# plankton/devices/linkam_t95/interfaces/stream.py
#------------------------------------------------------------

class LinkamT95StreamInterface(StreamAdapter):
    def __init__(self, device):
        # Tell StreamAdapter what the in/out line terminators are
        super(StreamAdapter, self).__init__('\r', '\r')
        self._device = device
        
    @stream_command('T')
    def getStatus(self):
        # Pretty much exactly like current getStatus in SimulatedLinkamT95, 
        # except accesses information it needs via self._device
        return ''.join(chr(c) for c in Tarray) 
        
    @stream_command('R1([0-9]+)')
    def setRate(self, rate):
        # Regex capture groups form arguments
        return ''
    
    # ... more stream_commands here
    
    @stream_command_default
    def handleError(self, stuff_that_didnt_match):
        # Called when none of the stream_commands matched, in case we want 
        # to handle errors... T95 happens to just ignore this quietly
        pass
        
    
class LinkamT95Device(CanProcessComposite):
    # This just creates and sets up a StateMachine 
    # Contains device methods, properties, attributes (previously Context)
    # No longer required to follow hardware interface
    pass

```

We'll have to work out how the Hardware combo class will work out. Particularly, since both the Device and Interface have a `process` method. 

Perhaps some simple intermediate classes `Interface`, `Device` and `Hardware` would help. Might be good for readability as well.


## Approvals

| Reviewer        |  Review Date          |
| ------------- |:-------------:| 
| Owen Arnold     | 5th September 2016 | 
| Michael Hart      | 5th September 2016       | 
| Michael Wedel | 5th September 2016      |  

The high-level design was approved by all parties 5th September 2016. As part of a 2 hour Skype meeting with the listed team above present. We also had input from Freddie Akeroyd.

## Decision
After thorough discussion of the suggestion, including aspects such as preserving the option to have different setups, controlling different aspects of the environment and the simulated device through an RPC-type approach, all parties were satisfied with the presented design.

The plan is to implement the changes incrementally and finish with all modifications by then end of the month, after which a version 1.0 tag will be added to the git repository.
