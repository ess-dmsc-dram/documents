# Investigation of Possible Instrument 2.0 Effects on Instrument View Performance.
This document outlines areas in which the performance of the instrument view may benefit from the introduction of the new Instrument 2.0 caching layers. Tests were carried out using the Microsoft Visual Studio debugger and profiling tools which provided information on which Instrument 1.0 methods are most heavily used when interacting with the instrument view.

### Parametrised Instrument Allocation
In several scenarios within the Instrument View (loading, switching between unwrapped views and picking) a parametrised version of the instrument is created before attempting to access detectors. Every call to `ExperimentInfo::getInstrument()` results in a call to `ExperimentInfo::makepParameterizedInstrument()`, which in turn is triggered by every call to `InstrumentActor::getInstrument()` or `ComponentActor::getComponent()`. For SANS2D, there are 255 calls to the parametrised instrument constructor, for GEM there are ~130K. Similar figures were recorded for switching instrument representations (unwrapped views). This seems to be, in general terms, a design flaw in Instrument 1.0. However, Instrument 2.0 obviates the need to access parameter maps or even the creation of a parametrised instrument. It therefore follows that any access which replaces this object creation with a table lookup could drastically improve performance.

### Caching Layer Lookup vs Detector Object Access
Following on from the last point, in most places where information about individual detectors are required, a pointer/reference to the detector object is obtained in order to retrieve detector id, shape, bounding boxes and corresponding workspace data. Instrument 2.0 simplifies this access by making most of this information directly accessible from the `DetectorInfo`/`ComponentInfo`. 

### List of Operations Instrument View requires of Instrument 1.0
- Parametrised instrument constructor 
- `Instrument::getDetector()`
- `Instrument::getSample()`
- `Instrument::getSource()`
- `Instrument::getDetectorIDs()`
- `Instrument::getBoundingBox()`
- `Instrument::getPhysicalInstrument()`
- `Instrument::setPhysicalInstrument()`
- `Detector::getRotation()`
- `Detector::getPos()`
- `Detector::getID()`
- `Component::getParent()`
- `Component::getComponentID()`
- `ObjComponent::getBoundingBox()`
- `ObjComponent::shape()`
- `ObjComponent::draw()`

### Considerations
- Is the current geometry renderer the best solution for Instrument View? Should the rendering be decoupled from the objects and abstracted away at a higher level? Perhaps a renderer which takes an instrument (`DetectorInfo`/`ComponentInfo`)and renders all (or a subset of) the components. Seems like visualization is mixed with in-memory representation. - ***"A renderer class which accepts a ComponentInfo and a list of component indices could be a good solution in order to create a more sensible code layout."***
- Why is `PickID` stored as some strange encoded colour? Couldn't some kind of map be built using the `DetectorID` directly so that on mouse over of a `ProjectionSurface` one could immediately retrieve the `DetectorID`? - ***"The pick color is a convenient way of addressing detectors using only 3 bytes (RGB ingoring Alpha) in OpenGL space. It makes it easier to handle mouse over on the visualized geometry. Detector IDs are sufficiently large to exceed the three bytes."***
- Will workspace indices be directly accessible from `DetectorInfo`? ***"Not necessarily, however, a map between detector indices/IDs can be built and used if necessary. Also, there is SpectrumInfo which maps spectrum index to detector indices in the SpectrumDefinition.***

### Recommendations

#### Calls to ExperimentInfo::getInstrument()

It seems as though calls to `ExperimentInfo::getInstrument()` are remnants of a legacy system where instrument geometry and associated parameter maps were always calculated on the fly. Since geometry is stored (in both Instrument 1.0 and 2.0) and the workspace observer mechanism allows for response to workspace updates, this is not at all necessary. These should be removed in favour of storing the `ComponentInfo/DetectoInfo`

#### Actors 

The actors seem to be a middle layer which wrap instrument, component and object operations. These layers interact with workspaces, parameter maps, store geometry and store colour (detector pixel intensity and pick colours). Roman believes with the new Instrument 2.0 layers `ComponentInfo/DetectorInfo` these may be redundant and in many cases may only act to slow things down. An example is in the constructor of `CompAssemblyActor` [here](https://github.com/mantidproject/mantid/blob/master/qt/widgets/instrumentview/src/CompAssemblyActor.cpp#L41) where there are several dynamic casts in a tight loop in order to check component type. Removing the actors would not only get rid of unnecessary overheads, but will create a more lightweight Instrument View widget solely concerned with displaying geometry and associated data. Instrument 2.0 layers already effectively and efficiently store all geometry in memory, even specifics like whether or not we are dealing with rectangular detectors.

#### Faster displays

Roman suggested using OpenGL display lists to speed up rendering although it seems like display lists are already extensively used for drawing the "actors" which store colour information. See [here](https://github.com/mantidproject/mantid/blob/master/qt/widgets/instrumentview/src/GLActorCollection.cpp#L39)


**NB** *There will be a follow-up issue which will outline a new sketch architecture for the instrument view. This document will be referenced from the issue*