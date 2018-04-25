## Draft Agenda

* Planning around MDWorkspace project for Dan Nixon (Everyone)
  * Outputs of Anton's work (in particular gathered requirements).
  * Ideas for single, ordered `MDEventList`
* EventList problem, few events (ESS SANS)
* Hardware requirements (Simon/Lamar)
  * What information has been gathered, which instruments, how have metrics been calculated, how can we reproduce?
* Onboarding new staff (Owen/Simon)
  * Plan projects, quite a few staff joining this year!
  * Organise meetings (see below)
* Group Meetings (Possibly All)
  * coverage for key and related events IKON, Nobugs, etc thoroughout the year
* Push forward Instrument questions template, probably won't get done unless we push for it. (Owen/Simon)
* Retrospective (see previous notes)
* Look at [Iteration 4](https://jira.esss.lu.se/secure/RapidBoard.jspa?rapidView=501&projectKey=DR&view=planning.nodetail). Decide what tracking approach would work best.
* Discuss mantid reevaluation 
* Workspace 2.0 rollout

## Plan for work for Dan

[TODO] white board photo to be placed here.

## Discussions with Voxels Detectors

### Cost of one Spectra per Pixel
* Compute overhead of processing individual pixels in a voxel bank.
* Overhead of the EventList 24 bytes per vector (WeightedEvent, RawEvent ...). Would currently have a unique EventList for every pixel. 
* Same compute and memory problem applies to Histograms too. 
### PeakFinding
* How to determine what detector a Q vector passes through (would be several) affects lots of the internals of `Peak` object
* May need to accumulate signal across several detectors in the same direction to form the peak. 
### Visualisation in InstrumentView
* Need to have some way of slicing the bank to view individual detectors (already known)
* Intensity of individual detectors would likely be very low

## New Starter
* Neutron training course [Lamar to add link]
* Understand Peak and PeaksWorkspace and use that in the context of the Workspace redesign. 
 * Could you represent a PeaksWorkspace in Dataset?
 * How could `Peak` be rewritten to better represent the physics needed?
 * Convert the `InstrumentRayTracer` to use `ComponentInfo`/`DetectorInfo`

## General 
* Generate a good understanding of crystallography within the team.
* Need to look at imaging and gather requirements as these feed into the hardware needs.
* [Template needs updating](https://confluence.esss.lu.se/display/DAM/Template+for+DMSC+page+in+instrument+wiki) propose titles for other groups (Owen Arnold)

## Workspace-2.0 (Dataset) rollout and ESS-Mantid strategy

See https://confluence.esss.lu.se/display/DAM/Workspace-2.0+rollout for notes from discussion.

## Harware Requirements for Live Reduction
### Main Task
* Lamar actioned to carry out this task
* Main question to be answered is how far we can push the live reduction (in terms of data rate) before we need MPI
* Pay attention to the following:
 * Instrument View (usability, responsiveness) in the absence of any processing step
 * Processing live reduction scripts.
 * Combination
 * Test with and without multi-threading, make note of any scaling presented by threading.
 * Is live listener keeping up with data stream?
* The idea is to start with skeleton reduction scripts which mimic each of the SANS, Powder Reduction and Inelastic reduction scripts. These will include the basic algorithms which are used.
* The complexity will be incrementally updated to match real workflows
### Background Task for general Hardware requirements
* Talk to developers in various technique areas as first port of call about hardware used on beamline:
 * Number of beamline computers and/or hardware configurations (clusters, VMs, Nomachine etc.)
 * Laptops and other remote sessions available to users.
 * Computer hardware used for reduction in offices.
 * Any other resources.

## Retrospective

### Start Doing 

* Informal chats at ISIS. Include Dan in with this.
* With more data reduction people might make sense to to do every other week as the DR group meeting separate from the DA group meeting.

### Stop Doing 

* Try to keep on topic. Avoid irrelevant noise.

### Continue 

- Good to continue every day
- Ensure that longer discussions happen offline
- Keep timings of meetings
- Doing on a need to meet basis

## Changes to Project Execution

* Backlog grooming agreed. Every 3 weeks.
* 4 column kanban board
* Done items pushed into "Release"
