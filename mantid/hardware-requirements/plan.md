# Estimating hardware requirements for data reduction at ESS

## Scope

### Live reduction

Preliminary/simplified on-the-fly reduction of data and visualization is a key promise of ESS and will be required for all instruments, any time the beam is on and at times probably also with beam of for other calibration work.

### Interactive reduction

The general view is that data at ESS will be so large that users cannot do data reduction at their laptop or desktop PC.
Therefore DMSC needs to provide resources for all interactive workflows using the Mantid GUI (`MantidPlot` or its successor) for data reduction and visualization.
This is required during a user visit as well as the time period after the experiment.
Furthermore, we need to provide access to such resources before an experiment such that users can familiarize themselves with the tools and provided software infrastructure.

- Due to the interactive nature, high CPU use will alternate with shorter or longer idle breaks.
  However, generally there will be a rather large permanent memory requirement, i.e., clustering interactive user sessions on a single compute node is only possible to a limited extent, and will require nodes with a large amount of memory.

### Script-based reduction

Reduction of data based on a (Python) script.
This covers auto reduction and batch reduction.

## What do we need

### Baseline

To establish a baseline, we need to survey the hardware used for data reduction at existing facilities using Mantid.
This should include computers at beamlines, laptops and desktop PCs used by instrument scientists and users, and cluster hardware resources.

### From instrument teams

- A similar reduction workflow (in Mantid) at an operating facility (should be ISIS or SNS) that we can use for benchmarking.
  - Could be several if the instrument has different operating modes.
- Listing of build-out phases including, for each phase:
  - Detector pixel counts.
  - Estimated typical event rates (should be given depending on accelerator power).
  - Typical length of a single run (single measurement for a given sample).
    Could be given as wall clock time or as event count.
- Other:
  - Are there large event-mode monitors?
    This is known to have caused issues at SNS.

## Result presentation

The results will depend on a number of variables.
Presentation as a spreadsheet is probably most useful, but auxiliary documentation is required.

### Required information

Most likely a heterogenos pool of hardware suits our needs best
The foll

- Disk I/O.
- CPU cores.
- RAM.
- Network.
- Do we need SSDs?

We need peaks and averages!

- Instrument.
  - Pixel counts
  - workflow
- Event rate.

- I/O (peak, total)
- SSD
- RAM
- CPU
- network

- factors between live reduction and other:
  - 2x or more (for vanadium, can, ...)
  - ?x in addition to that for other complexity?
  - I/O?

- all live reduction must be available simultaneously
- interactive reduction peaks during day times, and during an soon after phases with beam on (important during hot commissioning where we probably have short phases of beam with longer breaks?)
- do we need to "guarantee" a turnaround time for script-based reduction? For many applications getting results the next day may be too slow. Can this be handled via slow and fast queues?

- how many times is data reduced, typically? Depends on:
  - maturity of instrument and workflow
  - interactive vs. script-based
  - technique
  - stability of software
  - training and skills of the users
  - UX

## Tasks

1. Come up with some sort of questionnaire and run it by some friendly instrument scientist(s).
   Probably it would be better to run everything as interviews, i.e., *we* fill in the questionnaire?
2. Get an MPI build of Mantid running on the DMSC cluster.
3. Nexus event file loading benchmarks on the cluster.
4. Benchmarks of individual workflows.
   Probably not all needed in all details, can estimate based on similar workflows in some cases?


