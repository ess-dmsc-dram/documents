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
  1. Parallel workspaces which are easy, but don't have any computational scaling (to be investigated)
  1. Distributed workspaces which are hard to set up but might have a way of scaling horizontally.
* We need to take into account computational cost since we have 10 million pixels.
* We need to know how data reduction is performed for SCD, especially the protein case. Need to arrange a meeting with Fabio Orlandi ( I.P.)


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

  This means that MD algorithms are only used for peak integration and peak centring (which
  Sam will move into TOF). Magnetic investigations are not different to standard reductions.


### Interview with Alex B. and Duc L. 23/10/2017
* I asked the indirect group how multi-dimensional algorithms and data structures are
used within Mantid. Apparently they are not used at all. When the choppers are open and
a white beam becomes available, they perform the same steps as WISH. Else they use Horace and
there is not intention of moving away from that. However, *BinMD* and *ConvertToMD* is used in *MSlice*.


### Standup with Simon and Lamar 24/10/2017
* It was mentioned that we should investigate the principal scalability of the algorithms
  as we go through the list.


### Discussion with Steven, Simon, Lamar, Vickie, Andrei, Pete 24/10/2017
* typical SC inelastic work-flow is:
  * *LoadEventNexus* on data
  * Crop to the limits
  * *ConvertToMD* (converts to *MDEventWorkspace*)
  * *MDNormSCD* (converts to *MDHistoWorkspace*)
  * *PlusMD*, *DivideMD* (other arithmetic operations)
* MDNorm would not work on *MDEventWorkspace* well, since the norm would have to
be recalculated every time the box structure changes
* *MDEventWorkspace*'s prime purpose is visualization
* Requirement (independent of distributed system): would like to expose *MDEventWorkspace* to Python
* Vickie described the use case for SCD:
  * Similar to what is being done at ISIS
  * Corrections (spectrum correction, Lorentz correction, absporption correction) are applied on peaks but maybe should be applied on *MDEventWorkspace* (why?)
* *ConvertToMD* is quick in the US; they were surprised that it can take 10 minutes here for WISH
* MultiBlock (VTK) data set was mentioned as a distributed data set option
* We should check if *MDConvertToDiffractionMD* produces the same as *ConvertToMD* (with and without Lorentz correction)


### Standup with Simon and Lamar 25/10/2017
* Simon mentioned that the powder reduction at the SNS makes use of *CompactEvents*,
  which will reduce the number of events by creating weighted events out of events
  which are within a certain tolerance. The tolerance would be set by the resolution
  in the experiment. We need to check what the resolution of ESS instruments are.


### Interview with Pascal and Fabio 26/10/2017
* The reduction that was described matched pretty much what Sam had described earlier.
* From MD they use
  * *ConvertToDiffractionMDWorkspace* (which is very slow for them)
  * *IntegratePeaksMD* (but they think this algorithm is not working correctly; Sam is investigating)
  * *CentroidPeaksMD* (but very little, since the UB matrix is pretty good; also Sam is improving *CentroidPeaks*, hence it can be performed in TOF)
  * *IntegratePeaksUsingClusters* sometimes (this is purely event based)
  * *BinMD* (mainly via the SliceViewer)
* They stopped using *FindPeaksMD* and are now using *FindSXPeaks*
* They use the VSI a bit
* We should keep in mind that the data is recorded in histogram-mode
* Corrections and normalizations (Vanadium, Lorentz correction) are applied to
  the *MatrixWorkspace*
* When they perform diffuse scattering they might use *MDNormSCD* in the future
  and maybe merge runs. How and when this will happen is unknown now.
* The *PeakIntensityVsRadius* is used sometimes, but seems to produce erratic results. (Sam was informed)
* The resolution of WISH is 0.2 degrees and in the time domain dT/T = 0.006. They use logarithmic binning with about 5000 bins. They could use 32000 bins in the linear
case, but the buffer cannot handle this.
* **Very important**: They don't (and maybe) cannot make use of auto-reduction. They rely on seeing the data and changing the parameters. As such it is important for them to use the SliceViewer and potentially the VSI. This is also the reason they rely on *BinMD*. They mentioned that *SXD* operated in a similar manner. In addition they use the
*InstrumentView* quite heavily to manually correct the *PeakWorkspace* s. -> Can we support such a work-flow?


### Interview with Thomas L 30/10/2017
* Thomas provided the write up for his work regarding merging multiple runs of
  (diffuse?) single crystal runs which were measured at different rotations. The
  document can be found [here](https://github.com/mantidproject/documents/blob/alf_auto_alignment/Help/SingleCrystal/ALF%20Auto%20Alignment/ALF-Visualization.md) and the corresponding script [here](https://github.com/mantidproject/scripts/blob/master/development/ALF%20automation%20project/visualization/ALF_VisualizeMerged.py).
* The merge work-flow is very similar to what Andrei has described:
  ```
  def merge(rotation_matrix_ws, ...)
    ... # Standard processing of matrix workspaces
    md_histo_data_accumulated = new MDHistoWorkspace()
    md_histo_norm_accumulated = new MDHistoWorkspace()
    for rotation in rotation_matrix_ws:
      # 1. Convert each rotation in to MD
      md_event_ws = ConvertToMD(rotation, ...)

      # 2. Get the normalization and the binned data
      md_histo_data, md_histo_norm = MDNormSCD(md_event_ws, ...)

      # 3. Accumulate the data and the normalization
      md_histo_data_accumulated = PlusMD(md_histo_data_accumulated, md_histo_data)
      md_histo_norm_accumulated = PlusMD(md_histo_norm_accumulated, md_histo_data)

    # 4. Divide the data by the normalization
    out_ws = DivideMD(md_histo_data_accumulated, md_histo_norm_accumulated)
  return out_ws
  ```
* Again, there is no good reason to be in event mode. The normalization converts
  this into histogram-type data.
* The point of this work-flow is to add up slice-measurements.


### Interview with Alex 31/10/2017
* The inelastic work-flow is:
  * Perform reductions (with *MatrixWorkspace* s) which is then saved in the NXPSE format. The data is in histogram format and contains energy transfer on the x axis. All of this
  is done using the *MatrixWorkspace* facilities. Normalizations are done
  at this point too.
  * The next bit is done in Horace, but the equivalent in Mantid would be:
    * *ConvertToMD* applied to all workspaces
    * *MergeMD*
    * then slicing and fitting
* For the fitting *FitResolutionConvolutionModel* (TobyFit) and *Fit* with a Gaussian model are used.
* One of the things missing is a custom model for *FitResolutionConvolutionModel*.
* Other algorithms don't seem to be that important. Importance lies on fitting.


### Standup with Lamar and Simon 2/11/2017
* Simon mentioned that supporting fitting might be part of the work package. This
  means that multi-dimensional fitting needs to be considered.
* It was also mentioned that if a work-flow requires visualizations then this might
  become part of the work package.


### Standup with Lamar, Simon and Owen 3/11/2017
* We should look at the what needs to be done for interactive reductions
  * check single machine options
  * What are the elements that could cause head aches, e.g. rebinning in the *SliceViewer*
* We discussed resending batch jobs which reload partially processed data, i.e. save
  loaded and converted data via *LoadMD* and *SaveMD* (check cost of that)
  -> Could file-backed loading of event-type data work for the SliceViewer?


### Email from Esko 3/11/2017
* We want to know what the reduction work-flow for the ESS migth look like. Esko
  responded with:
  >The basic workflow for crystallography (be it X-ray or neutrons) consists of indexing, i.e. determining the unit cell and orientation matrix of the crystal (which requires having found some peak, not necessarily all), refining that indexing solution, predicting the positions of the reflections and integrating them, followed by putting them on a common (and eventually abosolute scale). In principle there is no need for an interactive workflow if an automated one works well enough (this is of course generally true…) An automated workflow also does not remove the need for diagnostic information (plots, statistics etc.) that the user would still want to see. The need for on-the-fly interaction of course also depends on execution times; if it only takes seconds to run the whole pipeline you don’t care, but if it takes days you might want to at least check what’s going on…

 This sounds pretty similar to what ISIS and the SNS are doing. There is no reason to
 believe that auto-reduction should work better for the ESS than for other facilities.
 As such we should work under the assumption, that unless there is a significant
 improvement of the algorithm fidelity within Mantid, they will require some sort of
 interactive, iterative work-flow.

### Skype call with Esko and Simon 7/11/2017

* Esko gave a detailed overview of how data reduction for SCD for macromolecular
  structures works. It requires some sort of indexing and determination of the unit
  cells. This includes of course peak finding but also peak prediction since some
  reflections are expected to be very weak. Other parts involve scaling of the data
  which I understood as some sort of normalization. Another important aspect is
  peak integration.
* All of this will have to operate in time-of-flight. Esko mentioned that when
  unit cells become large (>50 A) one gets more reflections which are closer
  to each other which can lead to errors in the Q space conversion (especially with
  moving detectors). However other SCD beamlines will have to operate in Q space.
* Data might be collected for weeks. It might well be that histograms are
  sufficient. Data sizes are 10s of GBs per file (that is one rotation).
* Visualization needs to be provided at least at the end of the reduction,
  in order to inspect the quality of the peaks that were found. If methods
  require user input/refinement then intermediate results need to be visualized,
  especially if things take a long time.
* The architecture they proposed carries meta-data along. This could include
  settings for some algorithms. Also this information needs to be included
  in the output of the data reduction, since data analysis might rely on this.
  The visualization does not have to be in 3D (Paraview itself not really required),
  but needs some *SliceViewer*-like feature, especially lambda-slices of the
  detector bank are of interest.
* Other solutions which are suitable for macromolecular SCD are:
  * [XDS](http://xds.mpimf-heidelberg.mpg.de/)
  * [MOSFLM](http://www.mrc-lmb.cam.ac.uk/harry/mosflm/)
  * [HKL3000](http://www.hkl-xray.com/hkl-3000)
  * [Dials](http://dials.diamond.ac.uk/about.html)
  * This would take 10s of people several years to write
* If there is an automated reduction pipeline then this has to be able to
  evaluate how well it has found categorized its peaks. The level of false-positives
  needs to be extremely low else users will loose trust.
* Corrections for sample holder peaks (or more general peaks which are generated not
  via the crystal) are normally handled by algorithms, i.e. automatically.
* Other packages which apparently do a good job are SXD2001

### Standup with Lamar, Simon and Owen 8/11/2017
* Simon reminded us that we discussed a n% sampling approach to determine how
  the data should be load-balanced. This seems like a good optimization for the
  Recursive Coordinate Bisection method which would default to that if n=100.

### Slack conversation with Simon 9/11/2017
* The contacts for inelastic beam-lines are Jon Taylor (indirect) and
  Pascale Deen (direct).

### Discussion with Alex 9/11/2017
* Alex explained the underlying data structure which is used in Horace to
  represent multi-dimensional data. It is essentially evenly gridded
  hypercube where each bin element points to a location of an event list.
  This event list can be stored on memory if the list does not fit into memory.
  The structure seems to be pretty much equivalent to an *MDEventWorkspace* where
  we set the level depth to 1 and ask for forced first-level-binning.

### Standup with Lamar and Simon 10/11/2017
* It was mentioned that the Space Filing Curve approach requires an in initial
  distributed structure. This is often an octree or some refinement mesh. constructing
  this (unbalanced) data structure can actually exceed the memory resources on a
  single node. Simon mentioned correctly that this might not be an issue, if
  we only use 1% of the data. Depending on the actual file size he is correct
  and we should therefore not discard this approach.


### Xavier Email 10/11/2017
* Xavier sent an email. Regarding the question if interactivity or auto-reduction
  will be required, he replied:
  >I think that both solution should be available. The way I see it, we will have a manual first pass on the data to constrain the reduction. In particular, automatic peak finding and UB matrix refinement often fails. This first pass allows to constrain the reduction. Once it is done, auto-reduction can kick in. It will end up in python scripting in the end (from the local contact point of view).

 The documents `xavier_info1.pdf` and `xavier_info2.pdf` indicate that the work-flows
 will be very similar to existing ones at other facilities.


### Discussion with Pascale, Simon and Owen 14/11/2017
* Pascale will be working on CSPEC which contains a 3D multigrid detector. She
  mentioned that events should be produced at a rate of 10TB/day with a single
  run taking up several TB. There are hundreds of runs that are stitched together,
  which would imply that we are dealing with 100+TB files. This would also mean
  that we would be collecting data on the order of tens of days. We need to
  double-check this
* The instrument specs are: 2.5x2.5x1cm^3 voxels on a 32m^2 detector area with
  depth of 16 voxels. Each neutron can loose up to 90% of its energy. There are 7
  to 14 incident wavelengths per pulse (either separated or combined)
* Some sort of visualization will be absolutely important both for Q-space data
  and data in instrument space. The later would be mainly used for diagnostic
  purposes of the instrument. The former (in form of the *SliceViewer*) is used
  to cut through the exitation spectrum. Of particular importance is the *LineViewer*. The visual inspection is used to determine when an experiment
  can be stopped. Also auto-reduction is not really an option for them, however
  everything up to the Q conversion can be done automatically.
* Data merging takes 1h which is too long.
* The way things are done at LET is a good indicator how CSPEC will be operating.
* Users will want to inspect and work in Q space, however instrument scientists
  will want to inspect the TOF workspaces too.
* Pascale will think about visualization requirements for TOF.
* It is very important to be able to look at sub-pulses.
* Mantid has shown instabilites and crahsed which can waist a lot of beam time.
* Pascale gave us an initial design specification document: `pascale_info_1.pdf`
* The data production is about 10TB per day when all wavelengths are used (this
  estimation is correct, when a wavelength width of 1Angstrom is assumed).

### Call with Gagik 14/11/2017
* `ROOT` stores data in the `TTree` data structure which is a heterogeneous
  multi-purpose data structure. Scientists build their own histograms or
  if they wanted other tree structures.
* Data is initially stored in `POOL` where it is pre-reduced.
* Does not look like `ROOT` has something like Mantid's MD system. That would
  normally be left to the user, since `ROOT`'s `TTree`' is more general purpose.


### Discussion with Alex 15/11/2017
* He thinks that for his case merging *MDEventWorkspace* files is better than
  merging *MDHistoWorkspace*, since at the required binning level, the event-based
  structure is 30x sparser.
* He also says that in the future people might want event-based workspaces for
  resolution calcualations.
* He mentioned that there is a concrete initiative to develop distributed
  Horace, which apparently has funding and should go ahead next year.
* Alex did have some ideas for a distributed event store. He suggests to
  have a hash map which represents a n-dimensional grid. The binning is defined
  by the number of representations that can be indexed with a `int64`. It is not
  clear how load-balancing would work on this.

### Discussion with Martyn 15/11/2017
* Martyn confirmed what Alex was saying regarding distributed Horace. It seems
  that users have a too long waiting time between measurements and publication.
  The PACE initiative aims to reduce that time. One of the aims is to
  look at a distributed Horace version, especially since instruments such as LET produce 500GB of merged data and with a new instrument in construction this will be 10x that amount. The reduction itself is happening on *MatrixWorkspace* objects,
  but the data fitting happens on the Horace side. If we were to convert
  the work that Horace does to Mantid, then we would have a conversion, merge
  and fit step.
