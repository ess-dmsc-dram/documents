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

Adapters are device owners.

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



### Option B

Detail design option B here.

#### Author Comments
The author may comment on any benefits or drawbacks in this section.

## Recommended Option
To be completed after design options evaluated by all parties.

## Approvals
To be completed after recommended option has been reviewed by all parties.

