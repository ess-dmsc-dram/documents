This document summarises project proposals to form a programme of work for the [Core Mantid Developement Team(s)](https://github.com/mantidproject/documents/blob/master/Project-Management/PMB/Mantid%20core%20team%20proposal.docx).
This document will be maintained and updated and prioritised as a [Mantid Technical Steering Committee](https://github.com/mantidproject/documents/tree/master/Project-Management/TechnicalSteeringCommittee) responsibility.

# 1. Read Standard NeXus Files

## Motivation
The NeXus [format](http://www.nexusformat.org/) is a well estabilished and critical file format for neutron data. That standard is undergoing change, with an early proposal for Geometry layout expected by September 2017. The new format will replace the string-based Instrument Definition File. 

1. **Performance**: relating to Instrument Definition processing has already been highlighted as an operational [requirement- Geometry 2016](https://github.com/mantidproject/documents/blob/master/Design/Instrument-2.0/requirements-v2.md#performance-as-a-non-functional-requirement) by a cross-facility delegation, owing to performance concerns.
1. **Correctness**: Mantid, at present, only load instrument definitions. A saved process nexus file, from a workspace that has been subject to an in-memory translation yields a incorrect geometry. 
1. **Cost**: As the nexus geometry is in embryo, cost of change is low, and we are invited to preview and try the new formats prior to ratification. Post rattification, our ability to influence the format, or request changes will be limited.
1. There is already momentum from the ESS to steer, define and use an updated format. There are economies of scale reasons for collaborating on this now. ISIS/ESS are prototyping the new format, summer 2017, with findings available to steer better estimates and inform benefits available mid September 2017.

## Specialist Skills Required
TODO
## Resource and Profile 
TODO
## Deliverables 
TODO
## Risks of Delaying:
* Cost. Delaying involvement will cost more time and effort. See Motivation.
* Correctness issues will remain. See Motivation.
* Performance issues will remain. See Motivation.
* The processed nexus format saved by Mantid is already not NeXus compliant. Delaying will put Mantid further behind.
* Technical debt. Old/legacy code for handling IDFs remains, with no future for replacement. 

