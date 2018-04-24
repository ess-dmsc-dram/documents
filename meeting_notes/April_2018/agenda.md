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

Two examples that are done or in progress:
1. `HistogramData`
   - A lot of effort, but big part also carried by team as maintenance effort.
   - Did not have the positive effect we had hoped for?
     Design heavily influenced by fitting the current way `Workspace2D` works.
     - `Workspace2D` not used for histograms.
     - New interface equivalent to old interface allowed for 1:1 change.
     - COW mechanism made interface complicated.
     - ...
2. Instrument-2.0
   - From the beginning we said that it is too much effort for ESS to carry out alone.
     - Nevertheless we did (apart from small contributions by others).
   - Not complete, despite having spent more ESS effort than planned:
     - Using old file format (converting back and forth when loading and saving).
     - `ParameterMap` still used.
     - Ray tracing, `Peak`, and `PeaksWorkspace` still used old instrument tree.
   - Majority of effort spent on integration with existing codebase and refactoring old code.
   
- How can we make the result better?
  How can use ESS effort more efficiently?
  - Rollout to algorithms of `HistogramData` and Instrument-2.0 maybe not necessary to full extent?
    Could have done a partial rollout (old interface are still in use anyway).

- `Dataset` rollout?
  - Rollout the replace `MatrixWorkspace` everywhere is completely unrealistic and undesireable.
    If we intented to do a rollout it would probably influence the design of Workspace-2.0 negatively, since a lot of compromises would be required.
  - Target less used workspace types and workspaces that currently piggyback on `MatrixWorkspace`.
    - Constant-wavelength (reactor) workspaces.
    - `TableWorkspace`.
    - `MaskWorkspace`, etc.?
  - Provide alternative to `Workspace2D` and `EventWorkspace` as well as alternative algorithms.
    - Need to establish early on that this is possible and does not have performance issues.
  - Provide conversion from `Workspace2D` and `EventWorkspace` to `Dataset`.
    This implies that we can use important algorithms like `LoadEventNexus`.
- Can we provide roadmap with intermediate tangible deliverables, such that we can motivate this for PMB and other facilities?
