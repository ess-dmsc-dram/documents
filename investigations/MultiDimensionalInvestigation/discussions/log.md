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
* typical SCD inelastic workflow is:
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
