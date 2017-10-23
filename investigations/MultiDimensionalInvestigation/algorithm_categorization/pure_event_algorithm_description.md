# Description of pure event type algorithms

In this document we want to describe MDAlgorithms which exclusively operate on
event-type workspaces. It is not intention to give an algorithmically exact
representation of the algorithms but rather to get a good understanding of their
functionality and their dependence on data-structure-specific features.


## Creation
* ConvertToDiffractionMDWorkspace
* ConvertCWPDMDToSpectra
* ConvertCWSDExpToMomentum
* ConvertCWSDMDtoHKL
* ConvertSpiceDataToRealSpace
* ConvertToDetectorFaceMD
* BoxControllerSettingsAlgorithm ( Base algorithm for ConvertToDetectorFaceMD, ConvertToMDParent, ...)
* ConvertToDiffractionMDWorkspace
* ConvertToMD
* ConvertToMDMinMaxGlobal (Helper algorithm for ConvertToMD)
* ConvertToMDMinMaxLocal (Helper algorithm for ConvertToMD)
* PreprocessDetectorsToMD (Helper algorithm for ConvertToMDMinMaxLocal and ConvertToMD)
* ConvertToMDParent(Base algorithm for ConvertToMD)
* ConvToMDBase (looks like it to me)
* CreateMD
* ImportMDEventWorkspace
* LoadSQW
* LoadSQW2
* OneStepMDEW

## Normalization
* MDNormDirectSC
* MDNormSCD

## Peaks

### IntegratePeaksHybrid

### IntegratePeaksMD

This algorithm performs integration of single-crystal peaks within a radius (with optional background subtraction) in reciprocal space.

##### Execution
1. Input: MDEventWorkspace, PeakWorkspace and peak radius settings
1. For each peak
  1. execute `integreateSphere` or `integrateCylinder` on the root level box. This yields
     information about the signal and error for the ROI and the inner and outer background,
      if this was specified.
  1. if a background was specified then normalize the background signal by the background volume
  1. Perform a signal correction with the background and save it in the information in the PeaksWorkspace.

##### Data Structure access
The `integreateSphere` method goes over all child boxes and checks if their vertices
are fully or partially contained in the integration region. If the box is fully contained
in the integration region, then the signal (and error) is added to the integrated signal,
if the box contributes partially, then the child box is recursively investigated. If the
box is not in the integration region, then it is not added to the total signal and not further
investigated.

##### Comment
The way we the data is stored in the structure should not matter to this algorithm.
Especially, having a parallel *MDEventWorkspace* would not be an issue here.

### IntegratePeaksCWSD
Integrate single-crystal peaks in reciprocal space, for *MDEventWorkspace* s from reactor-source single crystal diffractometer.

Specialized algorithm. TODO later (?)


### CentroidPeaksMD

Find the centroid of single-crystal peaks in a MDEventWorkspace, in order to refine their positions.

##### Execution
1. Input: MDEventWorkspace, PeakWorkspace and peak radius settings
1. For each peak
  1. execute `centroidSphere`  on the root level box. This will check down to the
  leaf level if the events are inside the peak sphere. If this is the case then,
  the events contribute to the total signal and weighted centroid position.
  1. The new values are added to the PeaksWorkspace and returned.

##### Data Structure access
The `centroidSphere` method access is comparable to `integrateSphere` for *IntegratePeaksMD*.

##### Comment
See *IntegratePeaksMD*




## Slicing
* SliceMD

## Other
* AccumulateMD
* GetSpiceDataRawCountsFromMD
* MDNormDirectSC
* MDNormSCD
* MergeMD
* MergeMDFiles

### Utility
* FakeMDEventData
