## Meeting Notes 13/02/2018

Attendees: Simon, Owen, Anton

### Items which were discussed and questions which were raised

### General discussion of the project
* Look again into event compression and check if this could be used to reduce
  data sizes
* We should add links in the current documentation to the SCARF installation
  scripts as well as tag the prototype branch and purge other branches
* We think that the `runID` is only used for `TobyFit`-related algorithms, but we
  need to check if this is true. We need to investigate if the `runID` could
  be removed from Mantid altogether (there is a chance that Andrei might
  be using it)
* When using the saved `MDEvent` workspace for visualization, we might need the
  capability to save out a slice of the data into a different file.
* We should go back to the comparison of the file-backed visualization and
  check if the limiting factor is given by the IO bandwidth of by the data
  reader speed.
* Using a multi-threaded `BinMD` for the file-backed reads might not be feasible.
  This needs to be investigated.
* If multi-threading is not an option for `BinMD`, we should investigate if
  multi-processing could be an option (using something like `boost::interprocess`)
* We need to change the estimates on SaveMD (this are likely to be higher)
* We should add an estimation for adding merging (of different rotations) to
  the distributed data structure
* `IntegrateEllipsoids`, `IntegratePeaksMD` and `FindSXPeaks` might have to
  be extended to receive MPI support. We should add an explanation how this
  can be done and how this changes the estimate. Additionally it was pointed
  out that volumetric detectors will be a complication for `FindSXPeaks` which
  will have to be investigated (one of the problems being that the signal might
  be smaller than the background, in which case we might need an algorihtm
  which operates in the MD domain). We discussed that the current approach of
  dealing with connected graphs might be a bottle-neck for a large set of peaks.


### Next steps

* Simon suggested to look at the current MD data structure and try to improve it
  by not tying the events to the boxes but by instead having a large event list,
  which is sorted in a z-order manner. Simon also suggested to look at event
  compression again. Owen and Anton agreed, considering that at this point it
  is uncertain if there will be any benefit from having a parallel file writer
  as the file system and its bandwidth are not known.
* A complication of the space filling curve is that it works nicely on integer
  data where for a z-curve bit-interleaving can be used to create an order.
  Depending on the number of dimensions this might require multiple integer values.
  However looking at standard resolutions, e.g. T-REX (20 $A^{-1}$/0.01$A^{-1}$=2000
  and 160 $meV$/20$\mu eV$=8000), means that we can represent these four dimensions
  quite easily by 16 bits which would give us of $2^{16}=65536$ steps per
  dimensions which easily satisfies the dynamic range of the instrument. This means
  that for 4D measurements we should be able to use a single 64bit integer. See
  also [here](https://github.com/cne1x/sfseize)
* We need to ask Jon Taylor how other dimensions, e.g. temperature or pressure are
  handled when recording the data. The main question is are different temperature
  measurements add into the same file?


### Going through code

* The strategy for the n%-sampling is currently set such that a fraction of the
  data is sampled which was measured in the first n% of the pulse time. This
  might not be the optimal approach and we should consider using the the first
  n% of data in each spectrum.
* The main bottle-neck for large data sets was the generation of the preliminary
  box structure. Simon suggested a recursive sampling approach similar to what
  we are currently doing. This should lead to a more distributed generation
  of the preliminary data structure.
* The measurements that we performed of the 40GB data set showed that
  we have 8*10^9 events which get converted in 50 seconds using 500 ranks. Note
  that 30 seconds of this is spent on the preliminary box structure creation and
  it is expected that this can be drastically reduced. Comparing this conversion
  speed with the data rate of $8*10^{11}n/day$ yields a ratio of produced events
  to converted events of $(8*10^{11}n/day)/($8*10^{9}n/20seconds$) = 0.06. We
  need to check what this ratio is for the loading algorithm and other algorithms
  which are used for the reduction.
