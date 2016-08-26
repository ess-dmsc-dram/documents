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

### Option A

Detail design option A here.

#### Author Comments

The author may comment on any benefits or drawbacks in this section.

### Option B

Detail design option B here.

#### Author Comments
The author may comment on any benefits or drawbacks in this section.

## Recommended Option
To be completed after design options evaluated by all parties.

## Approvals
To be completed after recommended option has been reviewed by all parties.

