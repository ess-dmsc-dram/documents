## Agenda

### Monday 2rd July
CR 24 10:00 - 18:00

#### Hardware Requirements 
* [Live Data measurements](https://github.com/DMSC-Instrument-Data/documents/blob/34b89eef0a9d064c6f0bb4746365ba3ed104d7ca/investigations/Live%20Reduction/LiveReductionInvestigation.md) and [PR](https://github.com/mantidproject/mantid/pull/22691) (Lamar)

#### Instrument Team Requirements
  * Imaging [sine2020](https://github.com/DMSC-Instrument-Data/documents/blob/8f3abf8cbc951a23e1d3eeeec0285c039cded9ed/meeting_notes/June_2018_Italy/imaging_questions.md)
  * Engineering [Beer](https://indico.esss.lu.se/event/1023/)

### Crystallography
* Discuss a shared resource pool (Sam will be absent). General agreement within SXD dev teams that concept development would be very useful and is badly lacking in Mantid.
* NXTools?

##### Discussions and Actions
1. See updated project plan
1. Need to build an understanding of this domain
1. Invest time in building necessary concepts for this domain

#### Introductions 

* ISIS SANS demo with Matthew (Monday afternoon)
* ISIS Reflectometry demo with Gemma (Monday afternoon)
* Meet ISIS IBEX Dev Team

### Tuesday 3rd July

* CR 22 08:00 - 11:00 (Mantid Workbench)
* CR 24 11:00 - 18:00

#### Workspace2
* Overview of Type Erasure (best design so far)
* Discuss roadmap to complete design and get in front of PMB for resourcing

##### Discussions and Actions

1. Type-erased prototype agreed to be the most promising design and future prototyping effort will focus on this design possibility.
1. Agreed that it is natural to combine the Instrument 2.0 (`ComponentInfo`, `DetectorInfo`, `SpectrumInfo`) concepts into `Dataset` would need an equivalent/replaced `ParameterMap`
1. Algorithms
    1. Based on [rollout strategy](https://confluence.esss.lu.se/pages/viewpage.action?spaceKey=DAM&title=Workspace-2.0+rollout) new "Algorithm" concept will be required. We could/should use this opportunity to rollout a new naming.
    1. We would like to get away from using Algorithms directly. Would much prefer to call plain-old-functions. Would need to ensure that logging, reporting, locking etc is handled automatically somehow.
1. Workspace 2.0 prototype intended for completion for end of 2018. 
    1. Ideally design should be screened by TSC. Not PMB job to comment on design, but benefits of new design will need to be explained
    1. Good argument for how rollout should happen. TSC should be involved in what that preferred strategy should be.
    1. Resource Estimates for first phases
    1. More examples needed for preferred use of `dataset` as there are several ways of doing things.
1. There is already a [TODO](https://github.com/mantidproject/workspace-sandbox/blob/dataset/doc/type-erased-prototype.md) however many performance benchmarks are still required.
1. Need to prototype numpy array exports


#### Mantid Workbench
Martyn to lead discussion on this. Slides [here](https://docs.google.com/presentation/d/15xS9bZqqOzbeoNatkrybtKfLSO-ytdtHbkWd8fe2SPA/edit?usp=sharing)

##### Discussions and Actions
1. Usability testing for workbench could be found from Thomas's group.
1. No immediate plans allowing us to switch to python 3.
1. Aiming for a January 2019 release of Workbench. Would include essential tools like SliceViewer as well as Scientific Custom Interfaces

#### MD Work
* Overview by Dan Nixon 
* How to continue resourcing this. PACE crossover etc. MD Work? 

#### Hardware Setup
* The [DAaaS](https://github.com/DMSC-Instrument-Data/documents/blob/master/meeting_notes/May_2018/DAaaS.md) Model - this has wider scope than Data Reduction. Should be discussed with Jon. For detailed discussion would need to involve SXD 

#### Dinner
The Wheatsheaf Inn, East Hendred, 6pm

### Wednesday 4th July
CR 11 08:00 - 15:00

#### Tours (mainly for Neil)
* Tour of ISIS (Wednesday 10:15 outside IBEX office)

#### Planning
* Look at [plan](https://docs.google.com/spreadsheets/d/16z5WiGysXqssw5GFhP05LpfEnmoU-sBeT-HiZSGOzAA/edit#gid=669025093) with Jon Taylor
  * New plan to include new staff if possible
  * Check plan over with everyone including Jon Taylor

##### Discussions and Actions
1. Regarding testing of `LoadEventNexus` MPI - Lamar to talk to Tobias about file system. Might be possible for Lamar to test on Diamond file system too. (2019) we should try to use Diamond setup.
1. Run through matrix of day 1 requirements for instruments and turn into plan before end of 2018? We can reprioritise based on instrument schedule over the summer. (See Master Schedule). Should have a better plan at the end of the year based on this. 
1. We need to understand things like State Objects carried through scripts in data reduction.
1. Need to establish if `dataset` helps with the reduction workflows themselves. Does time invested into dataset mitigate time spent dealing with for example State Object above which are probably unecessary with `dataset`.
1. Soft veto quite important need to find a way to work on that. 
    1. Need to work on Choppers and any other number of things. Accellerator terminated while generating pulse. Veto on target segment? On moderator temperature or state of moderator. 
    1. Live listener soft vetoing. Veto as part of the decoder as can be more efficient before Workpace creation? 
    1. How do you construct the filters - Does this come from Experiment control? Probably a good question for next workshop.
    1. Need to generate list of things that we would want as a standard filter.
1. See updated project plan.





