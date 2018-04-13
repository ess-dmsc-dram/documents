# Estimating hardware requirements for data reduction at ESS

## Scope

### Live reduction

Preliminary/simplified on-the-fly reduction of data and visualization is a key promise of ESS and will be required for all instruments, any time the beam is on and at times probably also with beam of for other calibration work.

### Interactive reduction

The general view is that data at ESS will be so large that users cannot do data reduction on their laptop or desktop PC.
Therefore DMSC needs to provide resources for all interactive workflows using the Mantid GUI (`MantidPlot` or its successor) for data reduction and visualization.
This is required during a user visit as well as the time period after the experiment.
Furthermore, we need to provide access to such resources before an experiment such that users can familiarize themselves with the tools and provided software infrastructure.

- Due to the interactive nature, high CPU use will alternate with shorter or longer idle breaks.
  However, generally there will be a rather large permanent memory requirement, i.e., clustering interactive user sessions on a single compute node is only possible to a limited extent, and will require nodes with a large amount of memory.

### Script-based reduction

Reduction of data based on a (Python) script.
This covers auto reduction and batch reduction.

## Prerequisites

### Baseline

To establish a baseline, we need to survey the hardware used for data reduction at existing facilities using Mantid.
This should include computers at beamlines, laptops and desktop PCs used by instrument scientists and users, and cluster hardware resources.

### From instrument teams

- A similar reduction workflow (in Mantid) at an operating facility (should be ISIS or SNS) that we can use for benchmarking.
  - Could be several if the instrument has different operating modes.
- Listing of build-out phases including, for each phase:
  - Detector pixel counts.
  - Estimated typical event rates, should be given depending on:
    - Accelerator power.
    - Initial vs. "final" moderator.
    - Detector build-out / coverage.
  - Typical length of a single run (single measurement for a given sample).
    Could be given as wall clock time or as event count.
- Other:
  - Are there large event-mode monitors?
    This is known to have caused issues at SNS.

## Result presentation

The results will depend on a number of variables.
Presentation as a spreadsheet is probably most useful, but auxiliary documentation is required.
The compute need should be given for individual instruments.
This will give us flexibility when the schedule changes.

### Required information

Most likely a heterogeneous pool of hardware suits our needs best.
In particular, the optimal balance between compute power and main memory will be different for interactive reduction and script-based reduction.
The main focus of the results should be:

- Number of required cores.
- Amount of main memory.
- Disk I/O.

Furthermore:

- Network.
  Likely not an issue, but  Ethernet is not sufficient in general.
  Infiniband or equivalent will do, even if not top-of-the-line.
- Some workflows may benefit from fast/large local SSD storage, in particular file-backed operation for working with `MDEventWorkspace`.
  It is currently not clear to what extent this would be used.

For all cases, we need to determine the requirements at peak times and averages.
For example:

- All live reduction must be available simultaneously.
- Interactive reduction peaks during day times, and during and soon after phases with beam on.
  This may be important during hot commissioning where we probably have short phases of beam with longer breaks?
- Do we need to "guarantee" a turnaround time for script-based reduction?
  For many applications getting results the next day may be too slow.
  Can this be handled via slow and fast queues?

### Variables

The required information listed above typically depends on a number of variables and parameters.
At least some of them are subject to change.

Key variables are:

- The instrument / technique, which defines the reduction workflow.
- Pixel counts.
- Event rate.

Furthermore, the required hardware depends on:

- The number of instrument scientists or users that need to work simultaneously.
- Various complexity levels of reduction workflows.
  For example, live reduction is cheaper than other reduction since the full or interactive reduction will also:

  - Reduce runs for normalization, such as vanadium or can runs.
  - Have extra complexity.
  - Save large project files.
  - Load large project files.
- Harmful interaction with other running reduction or analysis.
  For example:

  - If multiple remote desktop instances for data reduction are sharing the same compute node we will compete for local resources such as cache and memory bandwidth.
  - If the file system backend is very busy we will not reach our benchmarked I/O performance and thus waste CPU resources.

- The number of times a specific run is being reduced in practice.
  This depends on:
  - The technique area.
  - Maturity of instrument and workflow.
    Once everything works perfectly a single reduction (in addition to live reduction) may be sufficient, at least for some techniques, but in the first years of hot commissioning and operation we should expect a larger number.
  - Interactive vs. script-based reduction.
    Users may try reducing data several times before the workflow is settled and a working reduction sciprt is available.
  - Stability of software.
    For a new facility with new instruments we should expect crashes and the ensuing need to re-run the data reduction.
  - Training and skills of the users, UX, and automation of cluster access.
    If this is insufficient we may be wasting a lot of resources for:
    - Reducing data several times in the wrong way.
    - Script-based reduction on a cluster can easily waste lots of resources if the file sizes do not match the cluster partition size or if the reduction script is not sufficiently parallel for some reason.

## Initial tasks

1. Come up with some sort of questionnaire and run it by some friendly instrument scientist(s).
   Probably it would be better to run everything as interviews, i.e., *we* fill in the questionnaire?
2. Get an MPI build of Mantid running on the DMSC cluster.
   Needed for follow up tasks:
   - Nexus event file loading benchmarks on the cluster.
   - Benchmarks of individual workflows.
     Hopefully not needed for all instruments in all details, can estimate based on similar workflows in some cases?
3. Survey hardware used at ISIS and SNS for data reduction.
4. Establish limits (event rate) of non-MPI reduction, in particular live reduction.
   If we can (initially) run live reduction without MPI things become easier and requirements become easier to estimate.
