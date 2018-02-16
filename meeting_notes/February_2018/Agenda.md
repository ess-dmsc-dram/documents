## Draft Agenda for DMSC Visit to ISIS February 12th-16th 2018

Attendees, please update directly

## Key People and Availability
* Owen Arnold 12-16
* Simon Heybrock 12-15
* Lamar Moore 14-16
* Anton Piccardo-Selg 13-14
* Thomas Rod 15 only

## Arrival, Departure times, Accomodation Details, Other restrictions

### Simon 
Monday 12th until Thursday (full day).
### Thomas
Assumed to be available all day on the 15th.
### Anton
Will try to have anton available for at least 1-2 hours on the 15th
### Owen
Available all week except for Monday. I have been asked to talk about the ESS projects to a joint RAL computing group on that day.


## Agenda Items
* Retrospective for Current Working 

| Agenda Items        | Organiser           | Involves  | Details  | Duration | Date & Time | 
| ------------- |:-------------:| -----:|---------:| ---------:| ---------:|
| ~~Retrospective~~      | Owen | Simon, Lamar, Anton, Mike | Hold a retrospective. Would like as many developers as possible working on the project to contribute to that | 1 hr | 14th 13:00 |
| ~~MD Workspaces~~ | Anton   |  Owen, Simon, Lamar | Distributed md workspace review and planning | 1-2 days | 14th |
| ~~Project structure~~ | Owen   |  Thomas | Project management plans | 0.5 day | PM 15th |
| ~~Instrument Plans~~ | Owen, Simon   |  Thomas | Long-term plan. What needs to be done on instruments. Questions raised by Thomas | 0.5 - 2hrs | AM 15th |
| ~~Update estimates.xml~~ | Owen, Simon   | Thomas | Fresh estimates and updated 6-12 month plan | 0.5 - 1 hrs  | AM 15th |
| ~~Meet sponsors~~ | Owen   |  Thomas | Meet with Debbie Greenfield and Tom Griffin | 1 hr | 11:00-12:00 15th |
| ~~Imaging Requirements~~ | Owen/Thomas   |   | [flux normalisation](https://confluence.esss.lu.se/display/DAM/Imaging+-+Flux+normalisation), [calibration tools](https://confluence.esss.lu.se/display/DAM/Imaging+-+Calibration+tools) | 1 hr | 15th |
| Milestone Planning | Owen/Thomas | Simon | Thomas suggested this based on [this](https://confluence.esss.lu.se/display/DMSC/Overview+of+Milestones). Owen Arnold not familar with how this is done within the DMSC/ESS, so maybe best that Thomas leads the session. | 2 hrs? | PM 15th |
| ~~Workspaces~~      | Simon | Simon, Lamar| Simon working on this | 3 hr | 14th 13:00 |

## Meeting Notes

### Instrument 2.0, with Simon Heybrock and Lamar Moore, 15th February 2018

- Because we calculate the ComponentInfo on the base instrument, we can calculate the offset in makeLegacyParameter map without the need for the old Instrument tree itself.
- Can we get rid of scaleX, scaleY from Rectangular detectors. It looks like we could just use the existing scale factors in ComponentInfo to support this.
- Probably 1+ years of work to completely eliminate Instrument 1.0 from the codebase. The ESS can't justify the cost of this even though it is very desirable.
- Nexus Geometry means NOT creating Instrument 1.0 as the starting point. How do we do things like Instrument Ray tracing? Two possible approaches:
  1. Create Instrument 1.0 from Instrument 2.0 (easiest but essentially a HACK)
  1. Port code using Instrument 1.0 usage to 2.0. How much time would it take? Would be a significant task just to establish how much effort this would take.

### MD Distributed Data Reduction, Anton's Presentation, 15th February 2018

- Are tomography and imaging interested in this approach?
- New kitware tool?

### DA & DR Discussions with Thomas Rod and Simon Heybrock, 15th February 2018

- Use mcstas simulations as next phase for data reduction workflows. 
- Organised meetings at DMSC, with instrument scientists in 2018. Should ask about how familiar they are with Mantid.
- Need to establish where the current state of Mantid does not support their workflows. Missing Algorithms.
- May need to address the instrument teams 1:1, i.e. at next IKON. Maybe in Lund if not at IKON.
- Should make effort to understand Imaging requirements from Robin. ODIN should be a challenge.
- Are the errors going to be sqrt of counts?
- Imaging requirements (see Agenda) is already part of the discussion about normalising to monitors at the ESS.
- Thomas Delay changing any official milestones till after the instrument teams publish their plans.

## Retrospective 

Agreed points:

### Continue

* More paired development. Pointed out that this would particularly be the case at the start of new work. Furture examples might be the induction of Dan Nixon. Though this has already been done in the past.
* More time testing and reviewing for collaboration. At least some people felt that they were not keeping up to date with the general Mantid progress at other facilities.
* Short daily meeting. Though Anton pointed out that he quite liked the fact that these extend when needed so that the distributed team can talk about technical challenges.

### Start

1. Use the sprint/kanban boards to inform daily meeting. Try to keep up to date.
1. Longer term estimates. All agree that estimation is important and should be done properly. Owen Arnold will follow up. Longer term planning much harder because implicitly tied to unknowns such as facility and instrument schedules.
1. Have more user meetings. 
    * Create 1:1 sessions at IKON or in Lund with instruemnt teams
    * Form a good agenda of what information we want to elicit
    * Owen and Lamar to take more involvement going forward
    * Owen suggested generating quality requirements for each instrument that we can use on a repeated (yearly) cycle of updates
1. Generall call for more face-to-face time.
    * More time at DMSC/ESS from in-kind team
    * Team finds brainstorming useful
    * More informal catchups/coffee at ISIS and ESS
1. Split responsiblitites for going to meetings, but ensure that group consensus is represented and that key points make their way back to the whole group.

### Stop

1. Simon Heybrock raised: Sprints vs Kanban/backlog grooming "Short-term estimates and chunking into sprints does not look useful given our long-term project timescale". Owen Arnold disagrees with this last (quoted) point. We have agreed we will continue with 1 or 2 sprints and see what the concencus is about the usefulness.
