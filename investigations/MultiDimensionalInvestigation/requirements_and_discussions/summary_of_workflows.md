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


##### NMX

No will be not needing Q-space support

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

#### CSPEC

CSPEC will be operating in a verys similar way to CNCS and LET. From a sample
script that Pascale sent us we have extracted the entire workflow. It has
two parts. The actual reduction does not happen in the MD domain.

The reduction can be described as
1. Load vanadium data using *Load* (**MatrixWorkspace**)
2. Apply masking to the vanadium data set using *MaskBTP* (**MatrixWorkspace**)
3. For each measured run:
  1. Load the data using *LoadEventNexus* (**MatrixWorkspace**)
  2. Mask detectors using *MaskDetectors* (**MatrixWorkspace**). Note that the
     Vanadium workspace is used for this.
  3. Suggest background range for an incident energy *SuggestTibCNCS*. This
     will most likely be different in the new work-flow since this is CNCS-specific.
  4. Perform the actual reduction using *DgsReduction* (**MatrixWorkspace**)
  5. Set the goniometer settings on the reduced data *SetGoniometer* (**MatrixWorkspace**)
  6. Set the UB matrix *SetUB* (**MatrixWorkspace**)
  7. Convert to Q space using *ConvertToQ* (**MDEventWorkspace** and **MatrixWorkspace**)
  8. Save to file using *SaveMD* (**MDEventWorkspace**)

At this point the user has a set of hdf5 files which store a serialized
*MDEventWorkspace*. In the MD domain the following steps are performed:

1. Load vanadium data using *Load* (**MatrixWorkspace**)
2. Apply masking to the vanadium data set using *MaskBTP* (**MatrixWorkspace**)
3. Load each saved file using *LoadMD* (**MDEventWorkspace**)
4. Apply a normalization to each of the workspaces using *MDNormDirectSC* (**MDEventWorkspace** in and **MDHistoWorkspace** out). This step creates a binned data workspace and a normalization
workspace. Note that per workspace there might be several slices to process. Also
note that this algorithm essentially combines the workspaces, ie performs the merge
operation.
5. Divide the data by the normalization using *DivideMD* (**MDHistoWorkspace**)
6. Save the data, normalization and divided workspaces to file using *SaveMD*(**MDHistoWorkspace**)
