# Description of pure event type algorithms

In this document we want to describe MDAlgorithms which exclusively operate on
event-type workspaces. It is not intention to give an algorithmically exact
representation of the algorithms but rather to get a good understanding of their
functionality and their dependence on data-structure-specific features.


## Creation

There are many creational algorithms are many are very specialist. The main
algorihtm in use today is *ConvertToMD* which is quite difficult. Another
algorithm which is widely used is *ConvertToDiffractionMDWorkspace*.

#### ConvertToDiffractionMDWorkspace

There are several versions of this algorihtm the current version makes use
of *ConvertToMD*. However the early version of the algorithm is very intuitive
and illustates well what it actually means to convert a MatrixWorkspace into an
MDWorkspace, hence this is described briefly here.

Note that the algorihtm can accept a *Workspace2D* but it converts it into an
*EventWorkspace* with weighted events. Hence, it is fair to say that the
conversion only works on events. The event is characterized by the detector which
measured the event and the time-of-flight at which the event was measured. These
three dimensions are coverted into the three-dimensional Q space. The conversion
steps are:
1. Get the direction of the Q vector
  1. Get the normalized beam direction `beamDir` via the `Instrument::getInstrumentParameters` method
  2. Get the detector direction `detDir` via from the `SpectrumInfo::position` method
  3. Get the Q direction in the laboratory frame:  `Q_dir_lab_frame = beamDir - detDir`
  4. Potentially performa sign conversion, depending on the crystallography convention
  5. Convert from the laborarty frame to the sample frame or to HKL or leave as is,
     depending on the selected target frame. We end of up `Q_dir`
2. Calcualte the travelled distance: `distance = L1 + L2`
3. Calcualte the conversion factor: `wavenumber_in_angstrom_times_tof_in_microsec = mass_neturon * distance *1e-10 / (1e-6 * hbar)` which provides a conversion to
Q when the time-of-flight is in microseconds and the wavelength is in Angstrom.
4. Calculate the `wavenumber = wavenumber_in_angstrom_times_tof_in_microsec / event.tof()`
5. Calcuate the Q vector: `Q_dir=Q_dir *wavenumber`
6. The event weight and error are transferred one to one and the Q vector defines
    the position of the event.

In simple words:
First get the direction of the momentum transfer, which is defined by the incoming
direction and the direction the neutron has been scattered into. Second we need
to get the modulus of the momentum of the neutron (or rather wave number), which is
$k = m*v/\hbar = \frac{m*distance}{time_of_flight * \hbar}$.

While the real implementation is sligthly more complicated and can contain Lorentz corrections
etc, this is essentially what is happening for a diffraction conversion.


#### ConvertToMD

This the main conversion algorithm for going from time-of-flight to the MD domain.
Other conversion algorithms migth redirect to this algorithm under the hood. It is
also incredibly complex and hard to maintain and might pose a serious risk at any
rewrite effort. A very good starting place to undestand the algorithm can be found
[here](https://www.mantidproject.org/Writing_custom_ConvertTo_MD_transformation).

###### Structure

The algorithm is a general purpose conversion algorithm which allows developers
to add and register new conversions via a plugin system (dynamic factory pattern).
This is part why the algorithm is quite complex. However this complexity
mitigates from the actual conversion which is happening under the hood and in which
we are interested in.

The main conversion happens in classes which fullfil the *MDTransfInterface*
contract. As stated in the documentation the, the class has to perform two tasks:
1. Define the target MDWorkspace and its dimensions
2. Initialize the transformation and define the mapping from a standard event
   into the MDEvent (actually it is even more general than this since histogram types are allowed).

The main methods on *MDTransfInterface* are:

* `bool calcGenericVariables(std::vector<coord_t> &Coord, size_t n_ws_variabes)`:
   This used to set up generic coordinates of an event which depend on things
   like temperature, pressure etc. , i.e. quantities which can be found in the
   sample logs.
* `bool calcYDepCoordinates(std::vector<coord_t> &Coord, size_t i)`: This is
   used to set up coordinates which only depend on the individual detector
   position itself. This is partially used to setup some factors wich
   are used in other methods as in `MDTransfQ3D` and in `MDTransfModQ`. In
   `MDTransfNoQ` this is set directly
* `bool calcMatrixCoord(const double &X, std::vector<coord_t> &Coord, double &signal, double &errSq)`:
   This is takes care of the x axis data in the spectra. This is what converts
   the Q part. Most noteably, the `MDTransfQ3D` performs the same operation as
   the *ConvertToDiffractionMDWorkspace* in the elastic case.


Currently there are three plugins which define a transformation: `MDTransfQ3D`,
`MDTransfModQ` and `MDTransfNoQ` (when is this used?). The methods mentioned above
are chained in Template Method pattern where the resulting signals, errors and
coordinates are added to an empty workspace via the `MDxxxWSWrapper`.

One thing to note about all the conversion algorithms is that they occur on a
per-spectrum basis, which makes sense since events in a spectrum share the same
geometry.

The name of the `ConvToMDHistoWS` converter is confusing since it apparently converts
a *Workspae2D* into an *MDEventWorkspace*. At no point are we converting into
an *MDHistoWorkspace*.

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

#### MDNormDirectSC

The same as *MDNormSCD* but with some extras for the energy.

#### MDNormSCD

Calculates the normaliztion of an MDEvent workspace for SCD. The normalization
is the product of time integrated incident flux and the solid angle of detector
which contribute to the differential cross section at a point in q space.

###### Execution

The algorithm is very complex. As inputs it takes an *MDEventWorkspace* which contains
the counts, a *MatrixWorkspace* which contains the momentum-depenent input flux and
a *MatrixWorkspace* which contains momentum integrated solid-angle information (a Vanadium run).

```
def md_norm_scd(md_event_input_ws, flux_ws, solid_angle_ws):
  # The first thing that is done here, is to convert to MDHistoWorkspace
  output_md_ws = create_md_histo_output_ws(md_event_input_ws)
  normalization_ws = get_normalization_ws(output_md_ws)


  # For each detector we check what the space is that it occupies in Q.
  for detector in flux_ws.detectors():
    # Get the intersections of HKL planes with the space that detector
    # occcupies in Q and perform integration (code is not clear what the intention is)
    intersections = get_intersections(detector, normalization_ws, flux_ws)
    intersection_integrals = get_interesection_integrals(detector, flux_ws, intersections)

    solid_angle = get_solid_angle_for_detector(detecotr, solid_angle_ws)

    for intersection in intersections:
      position = get_average_intersection_position(intersection)
      normalization_signal = get_normalization_signal(intersection, intersection_integrals, solid_angle)
      normalization_ws.set_signal_at_position(position, normalization_signal)

  return output_md_ws, normalization_ws
```

This is a gross simplification of the algorithm. The main insight is the fact,
that we apply *BinMD* immediately, this could mean that we migth be able to
deal with histogram-type workspaces as the input.

###### Data Structure access
The event data structure has *BinMD* applied to it, hence we require the access
that *BinMD* requires. The resulting *MDHistoWorkspace* has indexed setter access
with an atomic add-operation

###### Comment on scalability and dependence on underlying data structure
The scalability is limited by the scalability of *BinMD*. In addition, the
atomic add-operation on the *MDHistoWorkspace* might also be a bottle-neck.

### Peaks

#### IntegratePeaksHybrid

Looking at the usage statistics for Mantid 3.5 to 3.9, this has not been used
heavily.

#### IntegratePeaksMD

This algorithm performs integration of single-crystal peaks within a radius (with optional background subtraction) in reciprocal space.

###### Execution
The algorithm can be described as below. This assumes the standard spherical case.

```
def integrate_peaks(peaks, md_ws):
  peak_ws = new PeakWS()
  for peak in peaks:
      box = md_ws.get_box()
      background_radius = get_background_radius(peak)
      signal, error = box.integrate_sphere(peak.radius)
      background_signal, background_error = box.integrate_sphere(background_radius)

      peak_corrected = get_corrected_peak(signal, error, background_signal, background_error)
      peak_ws.add_peak(peak_corrected)
  return peak_ws
```

The heavy lifting is done by `integreateSphere` or `integrateCylinder` on the root level
box. This yields information about the signal and error for the ROI and the inner and outer background, if this was specified.

###### Data Structure access
The `integreateSphere` method goes over all child boxes and checks if their vertices
are fully or partially contained in the integration region. If the box is fully contained
in the integration region, then the signal (and error) is added to the integrated signal,
if the box contributes partially, then the child box is recursively investigated. If the
box is not in the integration region, then it is not added to the total signal and not further
investigated.

###### Comment on scalability and dependence on underlying data structure

Ultimately the algorithm is interested in several patches of localized events, ie peaks.
This means that the sphere integration is a local operation.


#### IntegratePeaksCWSD
Integrate single-crystal peaks in reciprocal space, for *MDEventWorkspace* s from reactor-source single crystal diffractometer.

Specialized algorithm. TODO later (?)


#### CentroidPeaksMD

Find the centroid of single-crystal peaks in a MDEventWorkspace, in order to refine their positions.

###### Execution

The algorithm can be described as below.

```
def centroids(md_ws, peak_ws):
  peaks = peak_ws.get_peaks()
  for peak in peaks:
      box = md_ws.get_box()
      centre, signal = box.centroid_sphere(peak)
      normalized_centre = get__normalized_by_signal(centre, signal)
      peak.set_centre(normalized_centre)
```

The heavy lifting is done by `centroidSphere`  on the root level
box. This yields the signal and the centroid of the region of interest. The method
essentially checks down to the leaf level if the events are inside the specified
sphere. If this is the case then, then the events contribute to the total signal
and weighted centroid position.


###### Data Structure access
The `centroidSphere` method access is comparable to `integrateSphere` for *IntegratePeaksMD*.

###### Comment on scalability and dependence on underlying data structure
As with *IntegratePeaksMD* the data of interest for each peak is located in a small
region of the Q space. If there is a partitioning of the data in Q space then
it should be easy to execute this algorithm in parallel.


### Slicing

#### SliceMD

Creates a sub-workspace containing the events in a slice of an input *MDEventWorkspace*.
In contrast to *BinMD*, the space is not binned and the events are not summed up into
these bins.

Q: Why do we specify bins in the input? A: Because the *MDBoxImplicitFunction* function uses
the number of bins indirectly to determine the slice range.

###### Execution

The *SliceMD* algorithm is fairly complex

```
def slice_md(md_ws, slice_geometry):
  # Set up the output workspace
  out_ws = create_outut_ws()
  transfer_box_controller_settings_to_output_ws(md_ws, out_ws)

  # Define implicit function
  md_box_implicit_function = get_slice_function(slice_geometry)

  # Get all boxes which are contained by implicit box function
  top_box = md_ws.get_box()
  boxes = top_box.get_boxes(md_box_implicit_function)

  # Transfer events from input boxes to output workspace. We need to ensure
  # that the individual events are contained within the md box
  for box in boxes:
    if box is not masked:
        events = box.get_events()
        for event in events:
          if md_box_implicit_function.is_contained(event.centre):   
            out_box_centre = get_transformed_centre(box.centre)
            new_event = get_new_event(event, out_box_centre)

            # Add the new event to the top box of the output
            top_box_out = out_ws.get_box()
            top_box_out.add_event(new_event)

        # After having added teh events we might need to split the ws
        if out_ws.get_box_controller().requires_split(top_box_out):
          out_ws.split_all_if_needed
  return out_ws
```

Note that the specified binning is used when constructing the implicit MD box
structure, but only indirectly as we only use the number of bins.

###### Data Structure access
The algorithm performs a standard acces via the *getBoxes* method. The returned
boxes have been checked against an MD box-like structure, ie only boxes fully- or
partially contained in the structure are returned. Later on the events of these
boxes are added to another workspace via *addEvent*

###### Comment on scalability and dependence on underlying data structure
Leaving the current data structure aside, it would be possible to have this
scalable, since all we need to do is ask leaf nodes if they are contained within
a box-like structure. This is a local operation.

Adding events to the other workspace is currently highly nom-local since we
need to add them to the root box of the output workspace. However this is an
issue that we have for all algorithms which add data.

### Other
#### AccumulateMD
This algorithm appends new data to an existing multidimensional workspace.
It allows the accumulation of data in a single MDWorkspace as you go.

###### Execution
The *AccumulateMD* algorithm works as follows:

```
def accumulate(input_ws, data_sources):
  # Check if the data sources
  data_sources = remove_data_sources_which_are_already_in_workspace(input_ws, data_sources)

  if data_sources.is_empty():
    return

  merge_alg = new MergeMD()
  data_source_workspaces = load_data_source_workspaces(data_sources)
  output_ws = merge_alg.merge(input_ws, data_source_ws)
  return output_ws
```

###### Data Structure access
This is all abstracted to *MergeMD*.

###### Comment on scalability and dependence on underlying data structure
Same as *MergeMD*.

#### GetSpiceDataRawCountsFromMD
* specialist algorithm

#### MergeMD
Merges several *MDEventWorkspace* s into one, by adding their events together.

###### Execution
The merge algorithm operates on a list of workspaces and can be described as
below.

```
def merge(md_workspaces):
  output_ws = get_output_workspace(md_workspaces)
  for ws in md_workspaces:
    out_box = output_ws.get_box()
    top_box = ws.get_box()
    leaf_box = top_box.get_all_leaf_boxes()
    for bx in leaf_box:
      if bx is not masked:
        events = bx.get_events()
        out_box.add_events(events)
```

Essentially the algorithm finds all leaf nodes and adds the events to the
root level box of the output workspace. This is in a way pretty bad, since
the algorithm is very aware of the implemenation of the *MDEventWorkspace*.

###### Data Structure access
The entire data structre needs to be traversed and accessed. Teh underlying
data strucutre has its implementation details not abstrated away.

###### Comment on scalability and dependence on underlying data structure
The events need to be gathered from the entire q space and placed one by one into
the new data structure. It is not clear to me how scalable the merge really is.

#### MergeMDFiles
* Operates on files, so maybe not too relevant now.

#### Utility
##### FakeMDEventData
* not very relevant
