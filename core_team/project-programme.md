**Draft Pending TSC Approval**

This document summarises project proposals to form a programme of work for the [Core Mantid Developement Team(s)](https://github.com/mantidproject/documents/blob/master/Project-Management/PMB/Mantid%20core%20team%20proposal.docx).
This document will be maintained and updated and prioritised as a [Mantid Technical Steering Committee](https://github.com/mantidproject/documents/tree/master/Project-Management/TechnicalSteeringCommittee) responsibility.

# 1. Read/Write Standard NeXus Files

## Motivation
The NeXus [format](http://www.nexusformat.org/) is a well estabilished and critical file format for neutron data. That standard is undergoing change, with an early proposal for Geometry layout expected by September 2017. The new format will replace the string-based Instrument Definition File. 

1. **Performance**: relating to Instrument Definition processing has already been highlighted as an operational [requirement- Geometry 2016](https://github.com/mantidproject/documents/blob/master/Design/Instrument-2.0/requirements-v2.md#performance-as-a-non-functional-requirement) by a cross-facility delegation, owing to performance concerns.
1. **Correctness**: Mantid, at present, only load instrument definitions. A saved process nexus file, from a workspace that has been subject to an in-memory translation yields a incorrect geometry. 
1. **Cost**: As the nexus geometry is in embryo, cost of change is low, and we are invited to preview and try the new formats prior to ratification. Post rattification, our ability to influence the format, or request changes will be limited.
1. There is already momentum from the ESS to steer, define and use an updated format. There are economies of scale reasons for collaborating on this now. ISIS/ESS are prototyping the new format, summer 2017, with findings available to steer better estimates and inform benefits available mid September 2017.

## Blocking Projects
None
## Specialist Skills Required
TODO
## Resource and Profile Estimate
TODO
## Deliverables 
TODO
## Risks of Delaying:
* Cost. Delaying involvement will cost more time and effort. See Motivation.
* Correctness issues will remain. See Motivation.
* Performance issues will remain. See Motivation.
* The processed nexus format saved by Mantid is already not NeXus compliant. Delaying will put Mantid further behind.
* Technical debt. Old/legacy code for handling IDFs remains, with no future for replacement. 
## PMB Approval and Comments
### Approval Date 
### Comments

# 2. Leverage Instrument 2.0

## Motivation

The ESS and ISIS in-kind team has, thus far, provided 100% of the resourcing of the `Instrument 2.0` project. This has yielded more efficient and faster in-memory structures for all users, and core step-scanning changes required by the ILL. `Instrument 2.0` is explicitly described in the [SNS 5-year plan, section 4](https://github.com/mantidproject/documents/blob/master/Design/ORNL_Mantid_5yearplan.pdf)

1. We currently wrap aspects of Instrument 1.0, and created Instrument 2.0 based on Instrument 1.0, which is highly inefficient. Killing Instrument 1.0 would not only reduce the size of the code base, but also vastly improve in-memory performance and load/save times. This would first require extending and leveraging Instrument 2.0 for things such as shape related operations.
2. The ESS and ISIS in-kind team has extensively designed and prototyped features for Mantid, that are not a 1/1 replacement for `Instrument 1.0`, and will support new classes of real neutron instruments. These are described in Section 4.1.2 (Objectives) in the [SNS 5-year plan](https://github.com/mantidproject/documents/blob/master/Design/ORNL_Mantid_5yearplan.pdf) and include complex beam paths. Prototyping has signficantly de-risked these designs, and they are now ready to be put into production.

## Blocking Projects
None
## Specialist Skills Required
TODO
## Resource and Profile Estimate
TODO
## Deliverables 
TODO
## Risks of Delaying:
* Knowledge sharing. Understanding of the Instrument 2.0 long-term design and current implementations is entirely within the ESS Mantid team.
* Performance and memory requirements. `Instrument 1.0` is becoming an uncessary overhead. See Motivation.
* Technical debt around Geometry/Instrument. No other contingency plans to resolve this.
## PMB Approval and Comments
### Approval Date 
### Comments

# 3. Instrument Visualisation Performance

## Motivation

1. Visualisation at the instrument level has been requested by every instrument team engaed as part of the ESS/DMSC 2017 instrument-class coordination. The importance of visualisation prompted a deeper investigation and [report](https://github.com/DMSC-Instrument-Data/documents/blob/master/investigations/InstrumentView%20Performance/InstrumentViewInvestigation.md). That report advised that the `InstrumentView` had performance issues making it unsuable for instruments with over 600K detectors.
2. There is an increasing desire to use parts of Mantid imbedded in other applications. See Section 6.2 and 1.2 [ORNL 5-year plan](https://github.com/mantidproject/documents/blob/master/Design/ORNL_Mantid_5yearplan.pdf). The ORNL have already recognised that feed-back loops are critical aspects of these, and this has also observed this during Mantid/NICOS integration as part of the ESS direction.
. Section 2.2.1 ESS data-reduction-report. 
3. Usage statistics put the `InstrumentView` at the top of the list of Mantid's most used graphical interfaces.

In 2016, Mantid obtained the ability to run the `InstrumentView` without `MantidPlot`, and a python interface was provided. There has already been high level performance investigation work conducted by the ESS. The ESS will also contribute a deeper investigation of the performance. 

## Blocking Projects
Possibly project "Leverage Instrument 2.0" If Instrument reading is the major blocker.  
## Specialist Skills Required
TODO
## Resource and Profile Estimate
TODO
## Deliverables 
TODO
## Risks of Delaying:
* InstrumentView will be unusable for many ESS instruments such as CSPEC. Other facilities will be affected.
* InstrumentView cannot be be used as part of close feedback loops, such as with experiment control programs as is
## PMB Approval and Comments
### Approval Date 
### Comments

# 4 Distributed Data Reduction

## Motivation

In-situ data reduction, and increasingly large data sets require rapid processing at the Algorithm level. These factors are increasingly of concern to several facilities. The problems are particularly accute for Event mode processing.

Section 9.1 of the [ORNL 5-year plan](https://github.com/mantidproject/documents/blob/master/Design/ORNL_Mantid_5yearplan.pdf) outlines a desire to apply Mantid in heterogeneous distributed computing environements. This is also a featured in Section 2.2.3 ESS data-reduction-report 2017. 

For `MatrixWorkspaces`, a framework for this distributed approach is close to delivery. There is however a need to identify and port critical algorithms over to this way of working. Faclity specific algorithms are out of scope for this project.

## Blocking Projects
No other core projects block this 
## Specialist Skills Required
TODO
## Resource and Profile Estimate
TODO
## Deliverables 
TODO
## Risks of Delaying:
* Mantid will not be suitable for data rates produced by modern facilities
* Piecemeal approaches will not yield the overall performance required
* Attempting to solve framework performance problems at the last minute is risky at the operating facility level
* Mantid uses a range of ad-hoc/un-coordinated approaches for distributed computing
* The current knowledge of the framework level approaches is siloed to the ESS
## PMB Approval and Comments
### Approval Date 
### Comments


  

