# Discussion Outline -- Instrument-Specific Data Reduction

## Event Mode

What is required from event mode?
- Filter?
- Anything else here, or histogram right away?
- Is it required to hold a long history in memory, e.g., all events collected during the past 5 hours?
  - Runs take very long?
  - Need events for comparison of results during a long parameter sweep?


## Instrument

### Detectors

- New detector technology?
- What needs to be changed in data reduction?
  - ConvertUnits taking into account 3D nature
  - more?
- Calibration?
- Efficiency corrections?

### Monitors

- Event mode?

### Other

- Wavelength frame multiplication / pulse skipping, etc.?
- Moving or otherwise time-dependent components?
- Handled in same workspace or always separate?
- Do we need some sort of merging (workspaces with different instrument configurations)?


## Bringup (pre-operations)

What is required during bringup?

- Day 0?
- How will the instrument be calibrated?
  - Standard samples that might be run (larger than design "production" sample size -> more scattered neutrons)
- Later on?


Examples:

- Instrument view (what features?)
- Live reduction?
- Python scripts sufficient?


## Running the Experiments

### General

- Is there anything during a run that cannot be set up either automatically or before the run starts (interaction might be costly to implement if live reduction runs on a cluster)?
- What "live" feedback is required during an experiment run?
  - Instrument view with raw data?
  - 0D, 1D, 2D, 3D data (plots)?

### Integration with Experiment Control Software

- Anything special required?


## Algorithms

- Computational hotspots (mathematically expensive)?
- Rough overview of required algorithms (existing now in Mantid)?
- What new algorithms would be required?


## MDWorkspace

- Required for basic data reduction?
- Required for more advanced or later stages of reduction (analysis)?


## Files

- Many small files or few large ones?
  - Typical sizes and counts?
- Raw data vs. reduced data?
- If many small ones, is reduction for each one independent?

## Batch Reduction

- How often will an experiment constitute a single sample run?
- How can we identify special runs, such as transmission runs?
- Typically how many runs could be required as part of an experiment?

