# Algorithm Categorization

## Pure Histogram algorithms

### Creation
* ConvertToReflectometryQ
* CreateMDHistoWorkspace
* ImportMDHistoWorkspace
* ImportMDHistoWorkspaceBase (Base algorithm)
* ConvertMDHistoToMatrixWorkspace
* SaveZODS

### MDArithmetic
* AndMD
* DivideMD
* EqualToMD
* ExponentialMD
* GreaterThanMD
* LessThanMD
* LogarithmMD
* MultiplyMD
* NotMD
* OrMD
* PowerMD
* SetMDUsingMask
* WeightedMeanMD
* XorMD
* BooleanBinaryOperationMD (Base algorithm)

### Peaks
* IntegratePeaksUsingClusters
* IntegrateMDHistoWorkspace

### Slicing
* IntegrateMDHistoWorkspace
* SliceMDHisto
* ProjectMD

### Transforms
* ConvertMDHistoToMatrixWorkspace
* InvertMDDim
* MDHistoToWorkspace2D
* SmoothMD
* ThresholdMD
* Transpose3D
* TransposeMD

### Other
* SetMDUsingMask

### Utility
* CompactMD
* ReplicateMD

## Pure Event algorithms
### Creation
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

### Normalization
* MDNormDirectSC
* MDNormSCD

### Peaks
* IntegratePeaksHybrid
* IntegratePeaksMD
* IntegratePeaksCWSD
* CentroidPeaksMD

### Slicing
* SliceMD

### Other
* AccumulateMD
* GetSpiceDataRawCountsFromMD
* MergeMD
* MergeMDFiles

### Utility
* FakeMDEventData


## Mixed algorithms
### Creation
* SaveMD
* LoadMD

### MDArithmetic
* MinusMD
* PlusMD
* BinaryOperationMD (Base algorithm)
* UnaryOperationMD (Base algorithm for which the derived algorithms only work on MDHisto. Why accept both then?)

### Peaks
* FindPeaksMD
* IntegratePeaksMDHKL

### Slicing
* BinMD (but histogram needs link to original event or weighted workspace)
* CutMD (forwarding algorithm)

### Transforms
* MaskMD
* TransformMD

### Utility
* CloneMDWorkspace
* CompareMDWorkspaces

### Other
* SaveMDWorkspaceToVTK
* ChangeQConvention
* QueryMDWorkspace
* SetMDFrame



## Other algorithms or plain classes
* CalculateCoverageDGS (nothing to do with MDWorkspaces)
* FitMD (not clear what this does)
* Integrate3DEvents (Utility class; no direct dependency on MDWorkspaces, but maybe indirectly)
* IntegrateEllipsoids (for *MatrixWorkspace* only)
* IntegrateEllipsoidsTwoStep (for *MatrixWorkspace* only)
* IntegrateFlux (for *MatrixWorkspace* only)
* MDEventWSWrapper (plain class)
* MDTransfAxisNames + MDTransfInterface + MDTransfModQ + MDTransfNoQ + MDTransfQ3D(plain classes)
* MDWSDescription
* MDWSTransform
* SaveIsawQvector (why is this in vates?)
* UnitsConversionHelper
