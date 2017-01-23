# Scanning Development Meeting February 2017

## Attendees

Owen Arnold,
Ian Bush,
Simon Heybrock

## Main goal

**Find an adequate solution for maybe the last big hurdle for scanning and storing positions in `DetectorInfo`**:

A long series of hurdles and issues that we will face when moving position information from the old instrument into `DetectorInfo` have been overcome for the very similar case of masking (see https://github.com/mantidproject/mantid/pull/18318 and the list of linked issues). This will carry over 1:1 to position information with some additional effort for dealing with several parameters for rotations and positions.

However, there is one big difference: Masking was only really used on the detector level. In contrast, all components have positions and rotations. A lot of code within the current `Geometry` module works with this data. Access is typically on the component level, i.e., not necessary an entity that is currently part of an instrument.

For masking, we solved a similar problem for providing legacy support for Python exports (`IDetector::isMasked`). The method forwards to a `DetectorInfo` that is referenced from the `ParameterMap` in `IDetector`. This part will carry over to position information as well. However, not all detectors are parameterized and thus this will not solve the issue in this case. Furthermore, position is a property of components (not just of detectors) and the interface must be uniform (currently solved by virtuality).

Potential solutions:

- Keep storing positions in the base (unparameterized) detector, use positions from `DetectorInfo` if parameterized. Would this require ensuring that all parameterized detectors have a `DetectorInfo`, which is currently not the case?

- Store `DetectorInfo` in `Geometry::Instrument` instead of `ExperimentInfo`. Store a pointer to the `DetectorInfo` in `Geometry::Detector`?

- Introduce `ComponentInfo`, so we can transfer positions of *all* components, not just those of detectors (see prototype)?

## Agenda

### Scanning

- Supporting `IComponent::getPos()` (see description above).
  - Does the simplest solution work (pointer to `DetectorInfo` in `ParameterMap`, use base position of not available)?
  - Do we need `ComponentInfo`, or can that be added later?
  - Try starting off with (draft) implementation to uncover issues that we may have overlooked.
- Discuss and decide on a strategy for geometry (positions, rotations, and shapes):
  - Use `Eigen`!?
  - How much effort would it be to extract a new geometry module from the current one and port it to `Eigen`?
  - Python exports?
  - Is it possible to use `Eigen` only in `Beamline` and then do a conversion when dealing with other parts of Mantid (until everything is ported)?


### General (if time permits)

* Understand and find a better way to deal with `ExperimentInfo::mutableSpectrumInfo` [see here](https://github.com/mantidproject/mantid/pull/18460/files) description alongside implementation for that method.
