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
Neutron training course [Lamar to add link]

## General 
* Generate a good understanding of crystallography within the team.
* Need to look at imaging and gather requirements as these feed into the hardware needs.



