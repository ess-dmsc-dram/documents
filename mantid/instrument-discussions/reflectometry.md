# Reflectometry

Meeting 2017-05-11
- Hanna Wacklin
- Simon Heybrock

## General

- ISIS reflectometry is a good start
  - INTER -> FREIA
  - maybe POLREF -> ESTIA?
  - scripts should be accessible
- Cannot think of immidiate application/requirement for MDWorkspaces
- File handling can be only partially automated?
- Finding files and data in log files?

## Time dependence in experiments / Event Mode

- Quickly alternate between samples (ABCABCABCAB...)
  - Data must go into separate files and workspaces
- Stroboscopic measurements -> feasible statistics for fast processes
  - Parameter varies very quickly, repeatedly goes through same cycle
  - Combine events from different cycles that have the same value of parameter
  - Probably event mode gives us this feature automatically, if filter can deal with the rate and memory lets us accumulate long enough?
- Polarization, flipped, e.g., per pulse, must go into separate workspaces

## Other

- Coherent summing (along constant Q instead of theta)
  - Either curved sample, or less collimation in beam
  - More compute intense
  - Done at ILL by Robert Cubitt
  
## Instrument

- Detectors are 2D (has depth, but TOF correction done internally in detector?)
- 7x wavelength-frame multiplication at FREIA -> better resolution
  - no overlap in TOF -> overlap in lambda (convert separately then merge)
- Gravity correction
  - relevant of above 20 Å
  - affects angle of incidence
  
## Live
  
- Instrument view
- 1D or 2D live data (angle, TOF)

## Monitors:

- Long experiment: time normalized from detector
  - 4cm x mm at sample, then spreads out more -> hits strip of pixels, yielding of the order of 1e8 n/s/cm^2
  - used for simple normalization
- Per-pulse normalization required
  - Event mode, or time resolved histogram

## Future

- Detectors have depth, penetration depth is correlated to wavelength, might use that for corrections.
- Grazing incidence SANS, off-specular
- Integration with experiment control
  - measure until curve does not change anymore
  - detect errors, such as peak not where expected?
