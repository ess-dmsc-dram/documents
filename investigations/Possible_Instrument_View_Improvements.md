# Investigation of Performance Bottlenecks in the Instrument View.
This document outlines the performance bottlenecks in the instrument view loading which are a direct result of Instrument 1.0 geometry access. Tests were carried out using the Microsoft Visual Studio debugger and profiling tools in conjunction with `Callgrind` on Linux which provided information on which Instrument 1.0 methods are most heavily used when interacting with the instrument view. The instrumentation was taken for the duration of the creation of the `InstrumentWidget`.

## Findings
The following report contains results in terms of percentage inclusive time during the loading of an empty GEM instrument in the instrument view:

- 34% of time is spent doing dynamic casts in several places: 
	- [CompAssemblyActor::CompAssemblyActor](https://github.com/mantidproject/mantid/blob/7fa758ce336c6ac8ad590c6f3476311d28ed54b2/qt/widgets/instrumentview/src/CompAssemblyActor.cpp#L52)
	- [ParComponentFactory::create](https://github.com/mantidproject/mantid/blob/546b2eccbaf236fd217ccbd21573f88aa0272103/Framework/Geometry/src/Instrument/ParComponentFactory.cpp#L58)
	- [ComponentActor::isNonDetector](https://github.com/mantidproject/mantid/blob/7fa758ce336c6ac8ad590c6f3476311d28ed54b2/qt/widgets/instrumentview/src/ComponentActor.cpp#L69)
	- [Component::Component](https://github.com/mantidproject/mantid/blob/master/Framework/Geometry/src/Instrument/Component.cpp#L25)
- 49% of time is being spent on `InstrumentActor::getInstrument()` with the following breakdown:
	- 23.41%  [ExperimentInfo::getInstrument()](https://github.com/mantidproject/mantid/blob/master/Framework/API/src/ExperimentInfo.cpp#L218) where most of the time is spent calling `ParComponentFactory::createInstrument`
	- 11% `std::use_facet`
	- 6% `ConfigServiceImpl::getString`
	- 4% `sp_counted_base::release`
- Of the 25% inclusive time spent on calls to `ComponentActor::getDetector`, 17% is spent calling `InstrumentActor::getInstrument()`.

The results above clearly show that the majority of time is being spent in Instrument 1.0 geometry access. Even with the instrument being drawn on screen, the geometry access dominates the processing time.

## Interpretation 
### Copying Instrument Geometry
When creating the instrument view, the entire instrument geometry is copied and stored in "Actors", since the component assembly uses some kind of shoe-horned mechanism (poorly designed system of virtualisation), several dynamic downcasts must be performed in order to determine types. This can be improved in Instrument 2.0 since the type information is stored in the `ComponentInfo/DetectorInfo` layers without the need for dynamic casting.
 
### Parametrised Instrument Allocation
In several scenarios within the Instrument View (loading, switching between unwrapped views and picking) a parametrised version of the instrument is created before attempting to access detectors. Every call to `ExperimentInfo::getInstrument()` results in a call to `ExperimentInfo::makeParameterizedInstrument()`, which in turn is triggered by every call to `InstrumentActor::getInstrument()` or `ComponentActor::getComponent()`. For SANS2D, there are 255 calls to the parametrised instrument constructor, for GEM there are ~130K. Similar figures were recorded for switching instrument representations (unwrapped views). This seems to be, in general terms, a design flaw in Instrument 1.0. However, Instrument 2.0 obviates the need to access parameter maps or even the creation of a parametrised instrument. It therefore follows that any access which replaces this object creation with a table lookup could drastically improve performance.

### ComponentInfo/DetectorInfo Lookup vs Detector Object Access
Following on from the last point, in most places where information about individual detectors are required, a pointer/reference to the detector object is obtained in order to retrieve detector id, shape, bounding boxes and corresponding workspace data which in some cases may require `dynamic_cast`. Instrument 2.0 simplifies this access by making most (if not all) of this geometry information directly accessible from the `DetectorInfo`/`ComponentInfo`. 

### List of Operations Instrument View requires of Instrument 1.0
The list below is sorted by relative cost. Everything above ObjComponent has a relative cost > 10%.
- `Instrument::getDetector()`
- `Instrument::Instrument` (parametrized)
- `Instrument::getComponentByID`
- `ObjComponent::getBoundingBox()`
- `Detector::getRotation()`
- `Detector::getPos()` 
- `Instrument::getPhysicalInstrument()`
- `Instrument::setPhysicalInstrument()`
- `Component::getParent()`
- `Detector::getID()`
- `ObjComponent::shape()`
- `Instrument::getDetectorIDs()`
- `Instrument::getSample()`
- `Component::getComponentID()`

### Questions and Answers
- Is the current geometry renderer the best solution for Instrument View? Should the rendering be decoupled from the objects and abstracted away at a higher level? Perhaps a renderer which takes an instrument (`DetectorInfo`/`ComponentInfo`)and renders all (or a subset of) the components. Seems like visualization is mixed with in-memory representation. - ***"A renderer class which accepts a ComponentInfo and a list of component indices could be a good solution in order to create a more sensible code layout."***
- Why is `PickID` stored as some strange encoded colour? Couldn't some kind of map be built using the `DetectorID` directly so that on mouse over of a `ProjectionSurface` one could immediately retrieve the `DetectorID`? - ***"The pick color is a convenient way of addressing detectors using only 3 bytes (RGB ingoring Alpha) in OpenGL space. It makes it easier to handle mouse over on the visualized geometry. Detector IDs are sufficiently large to exceed the three bytes."***
- Will workspace indices be directly accessible from `DetectorInfo`? - ***"Not necessarily, however, a map between detector indices/IDs can be built and used if necessary. Also, there is SpectrumInfo which maps spectrum index to detector indices in the SpectrumDefinition.***

### Recommendations

#### Calls to ExperimentInfo::getInstrument()

It seems as though calls to `ExperimentInfo::getInstrument()` are remnants of a legacy system where instrument geometry and associated parameter maps were always calculated on the fly. Since geometry is stored (in both Instrument 1.0 and 2.0) and the workspace observer mechanism allows for response to workspace updates, this is not at all necessary. These should be removed in favour of storing const references to the `ComponentInfo/DetectoInfo`

#### Actors 

The actors seem to be a middle layer which wrap instrument, component and object operations. These layers interact with workspaces, parameter maps, store geometry and store colour (detector pixel intensity and pick colours). Roman believes with the new Instrument 2.0 layers `ComponentInfo/DetectorInfo` these may be redundant and in many cases may only act to slow things down. An example is in the constructor of `CompAssemblyActor` [here](https://github.com/mantidproject/mantid/blob/master/qt/widgets/instrumentview/src/CompAssemblyActor.cpp#L41) where there are several dynamic casts in a tight loop in order to check component type. Removing the actors would not only get rid of unnecessary overheads, but will create a more lightweight Instrument View widget solely concerned with displaying geometry and associated data. Instrument 2.0 layers already effectively and efficiently store all geometry in memory, even specifics like whether or not we are dealing with rectangular detectors.

#### Faster displays

Roman suggested using OpenGL display lists to speed up rendering although it seems like display lists are already extensively used for drawing the "actors" which store colour information. See [here](https://github.com/mantidproject/mantid/blob/master/qt/widgets/instrumentview/src/GLActorCollection.cpp#L39)


**NB** *There will be a follow-up issue which will outline a new sketch architecture for the instrument view. This document will be referenced from the issue*