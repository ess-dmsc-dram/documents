#  Existing work-flows that use MD data

Here we want to condense what we have been able to understand from speaking to
developers and instrument scientists regarding work-flows that touch the
available MD infrastructure.

### Single Crystal Diffraction

#### ISIS

For the single crystal diffraction group the work-flow can be summarized as:

1. Load, crop data and apply normalizations (**TOF MatrixWorkspace**)
1. Convert to Q space using *ConvertToDiffractionMDWorkspace*  (**MDEventWorkspace**)
1. Peak search with *FindSXPeaks* (**TOF MatrixWorkspace**)
1. Determine UB matrix (**PeaksWorkspace**)
1. Integrate peaks with *IntegratePeaksMD*  (**MDEventWorkspace**)  OR *IntegrateEllipsoids* (**TOF MatrixWorkspace**)
1. Correct centre position with *CentroidPeaksMD* (**MDEventWorkspace**)
1. Inspect and correct peaks in different visualizers, e.g. *SliceViewer*, *VSI* and *InstrumentView*. (**MDEventWorkspace** and **TOF MatrixWorkspace**)
1. Change settings, e.g. change peak radius and perform some steps again.
1. Once the result is satisfactory save the *PeaksWorkspace* for processing in analysis
   software.

##### SNS

1. Load and crop data (**TOF MatrixWorkspace**)
2. Apply calibration of detectors using LoadISAWDetCal
3. Convert to Q space using *ConvertToMD*  (**MDEventWorkspace**)
4. Peak search with *FindPeaksMD* (**MDEventWorkspace**)
5. Determine UB matrix with FindUBUsingFFT (**PeaksWorkspace**)
6. Index peaks using IndexPeaks (**PeaksWorkspace**)
7. Change Niggli cell to conventional cell and re-index (**PeaksWorkspace**)
8. Integrate peaks with *IntegratePeaksMD*  (**MDEventWorkspace**)  OR *IntegrateEllipsoids* (**TOF MatrixWorkspace**)
9. Inspect peaks in different visualizers, e.g. *SliceViewer*, *VSI* . (**MDEventWorkspace** )
10. Change settings, e.g. change peak radius and perform some steps again.
10. Once the result is satisfactory save the *PeaksWorkspace* and combine with other orientations for processing in analysis software.

### Inelastic

#### ISIS

The inelastic group uses Horace, but if they were to use the Mantid it would look like this:

1. Reduce several data sets (**MatrixWorkspace**)
1. Convert the data sets using *ConvertToMD* (**MDEventWorkspace**)
1. Merge the data sets using *MergeMD* (**MDEventWorkspace**)
1. Slice the data using *SliceMD* (**MDEventWorkspace**)
1. Users fit the data with Gaussian model using *Fit* or *FitResolutionConvolvedModel* (**MDEventWorkspace**)

#### SNS

This is mostly from Andrei and is in fact similar what Thomas reported:
1. Load and crop the data (**MatrixWorkspace**)
1. Convert to MD using *ConvertToMD* (**MDEventWorkspace**)
1. Create normalization workspace and get binned data using *MDNormSCD* (**MDEventWorkspace** in and **MDHistoWorkspace** out)
1. Apply the normalization using *DivideMD* (**MDHistoWorkspace**)
1. Extract signal and error arrays to work in Python
