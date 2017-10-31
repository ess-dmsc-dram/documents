# Project Log

### Conversations with Owen 19/10/2017
* Results of the MD calculations need to be consumed on a single node, since
  there are no plans of providing a distributed version of *MantidPlot*,
  the *SliceViewer* or the *VSI*.
* The Q resolution will be comparable with current Q resolutions. This means
  that the histogram representation of the data will fit into a single machine.
* At the end of the processing chain we have to end up with an *MDHistoWorkspace*.
* At the beginning of the processing chain we will have a distributed or
  purely local *EventWorkspace*.
* Datasets are large mainly because of an increased number of events. The number
  of detectors can also be a factor of 10 larger than we are currently dealing
  with.


### Stand up with Simon and Lamar 23/10/2017
* It is unclear (or not fully clear) how users will consume data
* Two approaches have been mentioned:
  1. Parallel workspaces which are easy, but don't have any computational scaling (maybe not)
  1. Distributed workspaces which are hard to set up but might have a way of scaling it horizontally.
* We need to take into account computational cost since we have 10 million pixels.
* We need to know how data reduction is performed for SXD, especially the protein case. Need to arrange a meeting with Fabio Orlandi ( I.P.)


### Interview with Sam 23/10/2017
* Interview with Sam regarding MD usage in SCD (WISH 680.000 detectors in histogram mode). Standard usage is
  1. Load raw data
  1. Crop data
  1. Peak search with FindSXPeaks. This is now done completely in TOF. (~ seconds)
  1. FindUB on the peak workspace
  1. Convert to MD using ConvertToDiffractionMDWorkspace (ConvertToMD under the hood) (~10 minutes)
  1. Peak integration, e.g. IntegratePeaksMD, IntegrateEllipsoids, ... PeakIntensityVsRadius is used to find initial guesses for the
  peak radius.
  1. CentroidPeaksMD
  1. Save Peak workspace to file.

  This means that MD algorithms are only used for peak integration and peak centering (which
  Sam will move into TOF). Magnetic investigations are not different to standard reductions.

### Interview with Alex B. and Duc L. 23/10/2017
* I asked the indirect group how multi-dimensional algorithms and data structures are
used within Mantid. Apparently they are not used at all. When the choppers are open and
a white beam becomes available, they before the same steps as WISH. Else they use Horace and
there is not intention of moving away from that. BinMD and ConvertToMD is used in MSlice.

### Standup with Simon and Lamar 24/10/2017
* It was mentioned that we should investigate the principal scalability of the algorithms
  as we go through the list.

### Discussion with Steven, Simon, Lamar, Vickie, Andrei, Pete 24/10/2017
* typical SC inelastic workflow is:
  * LoadEventNexus on data
  * Crop to the limits
  * ConvertToMD (converts to MDEventWorkspace)
  * MDNormSCD (converts to MDHistoWorkspace)
  * PlusMD, DivideMD (other arithmetic operations)
* MDNorm would not work on MDEventWorkspace well, since the norm would have to
be recalculated everytime the box structure changes
* MDEventWorkspace's prime purpose is visualization
* Requirement (indepenent of distributed system): would like to expose MDEventWorkspace to Python
* Vickie described the use case for SCD:
  * Similar to what is being done at ISIS
  * Corrections (spectrum correction, Lorentz correction, absporption correction) are applied on peaks but maybe should be applied on MDEventWorkspace (why?)
* ConvertToMD is quick in the US; they were surprised tht it can take 10 minuts here for WISH
* MultiBlock data set was mentioned as a distribued data set option
* We should check if MDConvertToDiffractionMD produces the same as ConvertToMD (with and without Lorentz correction)

### Standup with Simon and Lamar 25/10/2017
* Simon mentioned that the powder reduction at the SNS makes use of CompactEvents,
  wich will reduce the number of events by creating weighted events out of events
  which are within a certain tolerance. The tolerance would be set by the resolution
  in the experiment. We need to check what the resolution of ESS instruments are.

### Interview with Pascal and Fabio 26/10/2017
* The reduction that was described matched pretty much what Sam had described earlier.
* From MD they use
  * ConvertToDiffractionMDWorkspace (which is very slow for them)
  * IntegratePeaksMD (but they think this algorithm is not working correctly; Sam is investigating)
  * CentroidPeaksMD (but very little, since the UB matrix is pretty good; also Sam is improving CentroidPeaks, hence it can be performed in TOF)
  * IntegratePeaksUsingClusters sometimes (this is purely event based)
  * BinMD (mainly via the SliceViewer)
* They stopped using FindPeaksMD and are now using FindSXPeaks
* They use the VSI a bit
* We should keep in mind that the data is recorded in histogram-mode
* Corrections and normalizations (Vanadium, Lorentz correction) are applied to
  the MatrixWorkspace
* When they perfor diffuse scattering they might in the future use MDNormSCD and maybe merge runs. How and when this will happen is unknown now.
* The PeakIntensityVsRadius is used sometimes, but seems to produce erratic results. (Sam was informed)
* The resolution of WISH is 0.2 degrees and in the time domain dT/T = 0.006. They use logarithmic binning with
  about 5000 bins. They could use 32000 bins in the linear case, but the buffer cannot handle this.
* **Very important**: They don't (and maybe) cannot make use of auto-reduction. They rely on seeing the data and
changing the parameters. As such it is important for them to use the SliceViewer and potentially the VSI. This is also
the reason they rely on *BinMD*. They mentioned that *SXD* operated in a similar manner. In addition they use the
InstrumentView quite heavily to manually correct the PeakWorkspaces. -> Can we support such a work-flow?


### Interview with Thomas L 30/10/2017
* Thomas provided the write up for his work regarding merging mutliple runs of
  (diffuse?) single crystal runs which were measrued at different rotations. The
  document can be found [here](https://github.com/mantidproject/documents/blob/alf_auto_alignment/Help/SingleCrystal/ALF%20Auto%20Alignment/ALF-Visualization.md) and the corresponding script [here](https://github.com/mantidproject/scripts/blob/master/development/ALF%20automation%20project/visualization/ALF_VisualizeMerged.py).
* The merge workflow is very similar to what Andrei has described:
  ```
  def merge(rotation_matrix_ws, ...)
  ... # Standard processing of matrix workspaces
  md_histo_data_accumulated = new MDHistoWorkspace()
  md_histo_norm_accumulated = new MDHistoWorkspace()
  for rotation in rotation_matrix_ws:
    md_event_ws = ConvertToMD(rotation, ...)
    md_histo_data, md_histo_norm = MDNormSCD(md_event_ws, ...)

    md_histo_data_accumulated = PlusMD(md_histo_data_accumulated, md_histo_data)
    md_histo_norm_accumulated = PlusMD(md_histo_norm_accumulated, md_histo_data)

  out_ws = DivideMD(md_histo_data_accumulated, md_histo_norm_accumulated)
  return out_ws
  ```
* Again, there is no good reason to be in event mode. The normalization converts
  this into histogram-type data.
* The point of this workflow is to add up slice-measurements.

### Interview with Alex 31/10/2017
* The inelastic workflow is:
  * Perform reduction which is then saved in the NXPSE format. The data is in
    histogram format and contains energy transfer on the x axis. All of this
    is done using the *MatrixWorkspace* facilities. Normalizations are done
    at this point.
  * The next bit is done in Horace, but the equivalent in Mantid would be:
    * ConvertToMD
    * MergeMD
    * then slicing and fitting
* For the fitting there are *FitMD*, *FitResolutionConvolutionModel* (TobyFit), etc.
* One of the things missing is a custom model for *FitResolutionConvolutionModel*.
* Other algorithms don't seem to be that important. Importance lies on fitting.
