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

- Discuss `SpectrumDefinition`, as added in https://github.com/mantidproject/mantid/pull/18460.
- Supporting `IComponent::getPos()` (see description above):
  - Does the simplest solution work (pointer to `DetectorInfo` in `ParameterMap`, use base position of not available)?
  - Do we need `ComponentInfo`, or can that be added later?
  - Try starting off with (draft) implementation to uncover issues that we may have overlooked.
- Discuss and decide on a strategy for geometry (positions, rotations, and shapes):
  - Use `Eigen`!?
  - How much effort would it be to extract a new geometry module from the current one and port it to `Eigen`?
  - Is it possible to use `Eigen` only in `Beamline` and then do a conversion when dealing with other parts of Mantid (until everything is ported)? 
  - Python exports?
- Gather information on parameters that we need to extract from the `ParameterMap`.
- Figure out how to deal with remaining code that moves parent components, which will now require updating `DetectorInfo`:
  - Can everything be refactored to do moves via `DetectorInfo`?
  - Identify algorithms that do this. Are they all covered by the `ComponentHelper` or are there other cases?
  - Is it possible to catch (all) such moves (similar to the attempt of accessing the `masked` parameter in the `ParameterMap` -- we throw an exception if this happens).
  - Does `ComponentProxy` and `LinkedTreeParser` from the prototype make this easier? https://github.com/DMSC-Instrument-Data/instrument-prototype/blob/master/cow_instrument/LinkedTreeParser.h
- Saving scanning workspaces (`SaveNexusProcessed`).

### General (if time permits)

* Understand and find a better way to deal with `ExperimentInfo::mutableSpectrumInfo` [see here](https://github.com/mantidproject/mantid/pull/18460/files) description alongside implementation for that method.

## Minutes

- Override `IComponent::getPos` in `Detector`. Use positions from `DetectorInfo` cached in `ParameterMap` if available. Throws if scanning (will fail for `InstrumentView`), since access only with detector index (no time index).
- `ExperimentInfo::setInstrument(...)`: add optional argument to pass `Beamline::DetectorInfo`. This would be used to set a `DetectorInfo` with scan information.
- `SpectrumDefinitions` will be set via `MatrixWorkspace::setIndexInfo`.
- `Beamline::SpectrumInfo`:

  ```cpp
  Eigen::Vector3d SpectrumInfo::position(size_t) {
    Eigen::Vector3d pos(0,0,0);
    for ( const auto &index: spectrumDefinition) {
       pos += m_detectorInfo.position(index); // index is std::pair<det,time>
    }
    return pos/spectrumDefinition.size();
  }
  ```
  
- `DetectorInfo::setPosition(const IComponent &comp)`:
  - Use this for all movements (refactor where `ComponentHelper::moveComponent` is used).
  - Use something similar to `Instrument::getDetectorsInBank` to obtain all affected detectors and update their positions based on the relative change of the parent position.
  - Consequence: Moves will be more expensive, since `getDetectorsInBank` creates parameterized detectors and does dynamic casts (getting posisions will be cheaper in turn). Check with Anton if beam center finding is affacted by this.

- Support for more complex Geometry operations for scanning instruments? Use wrapper classes in `API`, e.g.,
  ```cpp
  double API::DetectorInfo::solidAngle(size_t index, size_t time, const V3D &observer) {
    Detector tmp(detector(index));
    // clear detector info pointer (or even pmap?) such that geometry calls on `tmp` will not fail.
    tmp.setDetectorInfo(nullptr);
    tmp.setPos(position(index, time));
    // also set rotation and update position accordingly
    return tmp.solidAngle(observer);
  }
  ```
 
### Roman
- Following up on the example above for `solidAngle`:
  - Adapt `InstrumentView` to support scanning instruments.
  - Consider using `DetectorInfo` as a first step, without scanning and time index.
  - Show all detector positions at the same time.
- Get an overview of geometry related code in `Geometry` module. What is actively used (and by what) in Mantid? What parts would we need to extract?
  
### MDWorkspaces

- Converting a scanning `MatrixWorkspace` to an `MDWorkspace`?

  - Could split `ExperimentInfo`, map time index to run number
  - Could add time index to `MDEvent`
  - Good testcase might be `ConvertToDiffractionMDWorkspace.v1`

- Creating a scanning `MatrixWorkspace` and converting it to and `MDWorkspace` might be cheaper than converting individual runs and using `MergeMD`.

### Scanning of non-detector components

- Cannot be visualized at the same time (would not make much sense anyway)
- Put slider in `InstrumentView`?

### Moving forward with Instrument-2.0 implementation

- Consider adding things like `ComponentInfo` (as prototyped) to `Beamline`, even if not in immediate use.
