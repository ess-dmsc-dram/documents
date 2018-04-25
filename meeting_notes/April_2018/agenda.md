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
- Lessons learned from `HistogramData` and Instrument-2.0 (see above):
  - Philosophy: If it needs to be different from how it works currently, we will not bend to make it compatible with how things work currently in Mantid.
  - Will not attempt to do a full rollout.
    Only support/port what we need (*not* 900 algorithms).
- Stages:
  1. Implement `Dataset` with basic operations, Python support, and converters from existing workspaces to `Dataset`.
     Probably useful for people doing scripting and just want to use Mantid for loading their data?
  1. Loading and saving `Dataset` (NeXus?).
  1. Support in basic widgets like `InstrumentView`.
     - Widget to visually inspect arbitrary datasets (arbitrary number of dimensions, arbitrary variables).
  1. Replace less used workspace types and provide new workspace types.
     - Need ADS integration and algorithm support.
     - Adding support for `Dataset` in existing algorithms may not be desirable.
       Need new algorithms with potentially the same name, select right variant based in input (workspace vs. `Dataset`), similar to how the `Load` dialog changes and calls different algorithms depending on the type of the input workspace.
- Can we realistically reach the point where we can support all ESS workflows based on `Dataset` and algorithm that support it?
  Will we be able to do so by the time we start writing ESS reduction workflows, or would we be forced to do so based on `MatrixWorkspace` first?
  - Do we need to support *all* existing widgets, including `mslice`, etc.?
  - Plotting support.
  - Basic algorithm toolbox.
  - Diffifult to estimate effort for algorithms based on what we see currently (different implementations, too high-level non-generic algorithms).
    Go with bottom-up approach:
    - Compose list of basic elementary algorithms.
    - Estimate how these can map to existing algorithm, how existing algorithm are split into multiple, or merged into a single one.

- How do we balance resources between implementing `Dataset`, changes that would be usable in both old and new way, and changes that would becomes wasted if we transition to using `Dataset`?
  - Do a risk analysis.
  
- How does `Dataset` (and the rollout ideas discussed above) address or not address the items discussed in https://confluence.esss.lu.se/pages/viewpage.action?pageId=262417179?

  1. 
     - Better Python support.
     - Should be reducing complexity by having fewer algorithms and simpler operations.
     - Big question: How can we have algorithms for `MatrixWorkspace` and `Dataset` in parallel in the GUI without confusing users?
  2.
     - Item for core team work has already been prioritized by PMB.
     - Current workspace type system not suitable for all science, Mantid has outgrown workspace type system.
       Should be possible to get support.
  3. See item 2.), but in principle problem may remain, unless core team actually gets resourced.
  4. We are proposing an incremental change.
     New code woulde slowly reach the point where more and more workflows can be supported.
     However, ultimately there would be a breaking change or decision to not use algorithms based on old workspaces types anymore.
  5. Will need to rewrite or refactor all basic algorithms to support `Dataset` as well as proving a better and more modular toolbox.
  6. Unchanged.
  7. How can we make sure that `Dataset` gets used, even before we reach to point of supporting the first "100" core algorithms and all important widgets?
     - Workflows with many small files but multiple periods could benefit.
     - Reactor sources (fixed wavelength workspaces).
     - Find power users willing to work with basic `Dataset` without a lot of supporting algorithms, i.e., mainly based on lower-level Python scripts.
     - Is development guided by and (partially) tested against existing algorithms and workflows sufficiently close to testing/running in production?
     - We just change the workspace, but a lot of other components like instrument and meta-data handling would be unchanged.
       That is, we should not compare the proposed changes to anything like a development from scratch.

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
