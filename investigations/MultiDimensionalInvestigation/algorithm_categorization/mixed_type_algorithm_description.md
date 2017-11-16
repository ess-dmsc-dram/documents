# Description of mixed-type algorithms

In this document we want to describe MDAlgorithms which operate on
event-type and histogram-type workspaces. It is not intention to give an
algorithmically exact representation of the Mantid implementations but rather to get a good
understanding of their functionality and their dependence on
data-structure-specific features.

# Mixed algorithms

### Creation

#### SaveMD
This is discussed [here](./load_and_save.md)

#### LoadMD
This is discussed [here](./load_and_save.md)

### MDArithmetic
##### MinusMD

The *MinusMD* algorithm is used to subtract two workspaces.

###### Execution

In the case of *MDHistoWorkspace* subtraction the binning and dimensionality
needs to match between the two workspaces. The signals of the two workspaces are
subtracted from each other and the squared errors are added.

In the case of *MDEventWorkspace* subtraction, the work-flow below is used:

```
def subtract(ws1, ws2):
  ws_copied = ws1.clone()
  top_box = ws_copied.get_box()
  top_box2 = ws2.get_box()

  boxes = top_box2.get_boxes()
  for box in boxes:
    copied_box = box.clone()
    copied_box.set_signal(-1 * box.signal)
    top_box.add_event(copied_box)

  ws_copied.split_all_if_needed
  return ws_copied
```

###### Data Structure access
The data structure access is the same as with most algorithms. We access
via `getBoxes` (all leaf nodes) and place via `addEvent`.

###### Comment on scalability and dependence on underlying data structure
In principal this could be a scalable operation since the subtraction is local.
So in principal, with a different data structure there is no reason why this
should not be scalable.

##### PlusMD
This is the same as *MinusMD*, but we don't use the inversion of the signal value.
The same considerations regarding the scalability apply here.

##### BinaryOperationMD
 * Base algorithm

##### UnaryOperationMD
* Base algorithm for which the derived algorithms only operate on histogram-type data. Why accept both types of workspaces as inputs then?

### Peaks
##### FindPeaksMD
This algorithm is widely used at the SNS and has until recently been in use at
ISIS. ISIS SCD has switched in the last couple of months to *FindSXPeaks*. The
algorithm will be one of the bottle-necks to port to a distributed system,
since it is conceptually tied to the underlying data structure. Other
data structures will not work with this algorithm.

###### Execution

The histogram-mode case iterates over all bins and adds information about that
bin to vector of candidates if the bin's signal density is above a certain threshold.
The pre-selected boxes are then evaluated against each other and only boxes which
are not too close to each other (determined by a fraction of the peak radius)
are kept. The boxes are sorted via their signal strength and only the N boxes
with the most intense signal are kept and added to a *PeaksWorkspace*. The execution
is described below:

```
def find_peaks_histo(ws, threshold, tolerance, max_number):
  # 1. Get all bins above a certain threshold
  above_threshold = []
  for i in range(0, ws.get_number_of_bins()):
    if ws.get_signal(i) > threshold:
      above_threshold.append(ws.get_bin(i))

  # 2. Select bins which are not too close to each other
  unique_bins = []
  for bin in above_threshold:
    can_add = True
    for unique_bin in unique_bin:
      if is_too_close(bin, unique_bin, tolerance):
        can_add = False
        break
    if can_add:
      peaks.append(bin)

  # 3. Sort and select max number
  peak_ws = new PeakWorkspace()
  sort(unique_bins)

  # 4. Convert bins to peaks and add to peak workspace (only the top N bins)
  peaks = []
  for bin in unique_bins:
    peaks.append(convert_to_peak(unique_bin))
  add_top_bins_to_peak_workspace(peaks, peak_ws, max_number)
  return peak_ws
```

The event-mode case is very similar in nature. It can be described as
```
def find_peaks_event(ws, threshold, tolerance, max_number):
  # 1. Get all boxes which are above a certain threshold
  top_box = ws.get_box()
  boxes = top_box.get_boxes() # Gets all leaf nodes
  above_threshold = []
  for box in boxes:
    if box.get_signal() > threshold:
      above_threshold.append(box)

  # 2. Sort the boxes. Note that in the actual implementation a map (with an underlying
  #    self-balancing tree) is used, hence no explicit sorting is required. This
  #    is only to show the algorithmic significance of sorting at this step.
  sort_descending_order(above_threshold)

  # 3. Select the boxes which are not too close to each other and only up to
  #    the maximum number of boxes
  unique_boxes = []
  for box in above_threshold:
    can_add = False
    for unique_box in unique_boxes:
      if is_too_close(box, unique_box):
        can_add = False
        break
      if can_add:
        unique_boxes.append(box)  

    # We are not interested in all boxes.
    if len(unique_boxes) >= max_number:
      break

  # 3. Add peaks to peak workspace
  peak_ws = new PeakWorksapce()
  for unique_box in unique_boxes:
    peak = convert_to_peak(unique_box)
    peak_ws.add_peak(peak)
  return peak_ws
```

###### Data Structure access
Data structure access is as usual via `getBoxes` which returns all leaf nodes.

###### Comment on scalability and dependence on underlying data structure
While the `getBoxes` access is the same as in other algorithms, the sorting
of boxes is highly non-local. However, a distributed *Mergesort* lends itself
quite well to this problem.

A more serious problem is that if data which contributes to the same volume
in Q space is located on different ranks (and forms a peak) it might not be
considered as a peak in this sorting procedure.

Additionally we are comparing all peaks with all found peaks to check for neighbours
which we potentially don't want to count twice (if they are within a specified tolerance)
of each other. This means potentially that ranks need to communicate quite heavily
with each other.

All of this makes this one of the hardest algorithms to realize in a distributed
environment, which is not surprising since the concept of the algorithm is
heavily linked to the implementation details of the workspaces (this might
be the only algorithm which mentions the workspaces box structure  in the algorithm documentation).


##### IntegratePeaksMDHKL
Going by the usage statistics, this does not seem to be used very much, hence
we don't consider it now.

### Slicing
##### BinMD
This algorithm takes an *MDEventWorkspace* and bins into into a dense,
multi-dimensional histogram workspace (*MDHistoWorkspace*). Alternatively one
can provide an *MDHistoWorkspace* as the input if it contains a link to the
generating *MDEventWorkspace*, hence it is probably fair to say that this is
actually a pure *MDEventWorkspace* algorithm.

###### Execution
The algorithm is closely related to the *SliceMD* algorithm and accepts the same
kind of inputs. *SliceMD* however extracts the box structure that matches an
implicit function defined by the bin boundaries and places the events of these
boxes into a new *MDEventWorkspace*. In the *BinMD* algorithm  we effectively
reduce the events into bins. The algorithm operates as follows:

```
def bin_md(md_ws, binning):
  # 1. Get hold of an event-based workspace
  if md_ws.is_histogram and md_ws.has_original_event_workspace():
    throw ValueException
  elif md_ws.is_histogram and md_ws.has_original_event_workspace():
    in_ws = md_ws.get_original()
  else:
    in_ws = md_ws

  # 2. Generate a histogram-type output workspace
  out_histo = generate_output_workspace(binning)

  # 3. Fill the bins of the output. This is done in parallel by parcelling
  # the parameter space. This is presented here in a very stylized way
  chunks = get_parcelled_space(binning)
  for chunk in chunks:
    top_box = in_ws.get_box()
    implicit_chunk_function = get_chunk_function(chunk)
    boxes = top_box.get_boxes(implicit_chunk_function) # Get all leaf nodes
                                                       # that are in the chunk's region
    # If it is masked, we don't consider it
    if not box.is_masked():
      bin_box(box, out_histo, chunk)

def bin_box(box, out_histo, chunk):
    # 1. Check if the box is fully contained in a bin. Note that in the algorithm
    #    this is done on the raw array, which is not very scalable,
    #    but that implementation should be easy to change.
    if is_box_in_single_bin(box, out_histo, chunk):
      add_full_box_to_bin(box.get_signal(), box.get_error(), box.get_centre(), out_histo)
    else:
      # If the box is not entirely in the chunk region, then we need to go through
      # all events individually
      events = box.get_events()
      for event in events:
        if is_event_in_chunk_region(event, chunk):
          add_event_to_bin(event.get_signal(), event.get_error(), event.get_centre(), out_histo)
```

###### Data Structure access
The data structure access is the same as with most algorithms. We access
via `getBoxes` (all leaf nodes).  On the *MDHistoWorkspace* side we access the
raw arrays which is not very scalable, but can be adapted.

###### Comment on scalability and dependence on underlying data structure
This algorithm has several challenges in terms of scalability:
* the `getBoxes` access (which is the same for all other algorithms)
* the mapping from boxes to bins is potentially non-local (imagine the case of a single bin).
  atomic writes might be needed since (potentially) several ranks can contribute to the
  same bin.

##### CutMD
This is a forwarding algorithm which at the end of the day relies on *SliceMD*.

### Transforms
##### MaskMD
The algorithm masks all data in a rectangular block on an *MDWorkspace*.

###### Execution
The user specifies extents in the dimensions she wants to apply masking. Several
boxes can be specified. The box specifications are grouped on a per-box basis.
Per box the `TMDE(void MDEventWorkspace)::setMDMasking(Mantid::Geometry::MDImplicitFunction *maskingRegion)`
for *MDEventWorkspace* or `void MDHistoWorkspace::setMDMasking(Mantid::Geometry::MDImplicitFunction *maskingRegion)` for *MDHistoWorkspace*
are called.

In the case of the histogram-type workspace, the algorithm iterates over all
elements and checks if it is contained in the implicit function. If this is the
case, then the bin is masked. Since we do this for each masking group, we could
improve this by providing a *MDImplicitCompositeFunction* which would reduce the
times that we have the traverse the data structure.

The case for *MDEventWorkspace* is described below:

```
def mask_md(ws, implicit_mask_function):
  top_box = ws.get_box() # Note that since this is actually a method on the ws,
                         # we don't have to do this.

  # We only get leaf nodes which are in the masking region
  boxes = top_box.get_boxes(implicit_mask_function)
  for box in boxes:
     box.mask()
```

The retrieval of all the boxes that matches a certain implicit function is a
common access pattern for *MDEventWorkspace*, hence this algorithm does nothing
unusual

###### Data Structure access
The data access is via the `getBoxes` method with an implicit function in a
similar way to a lot of other algorithms.

###### Comment on scalability and dependence on underlying data structure
This is again a fairly local operation (we know which q region we want to mask).
It has the same constraints as other algorithms that use `getBoxes`, e.g. *MinusMD*.

#### TransformMD
This algorithm provides a linear transformation, i.e. offset and scale for each
dimension in an *MDWorkspace*.

###### Execution
The algorithm changes the relevant entries in the *MDHistoDimension* of the workspace.

If the algorithm is an *MDHistoWorkspace*, then there is nothing left to do, unless
the scaling was negative in which case the raw signal array is inverted. This could
be an issue if we wanted to have a distributed *MDHistoWorkspace*, but that
would depend on the implementation details.

If the algorithm is an *MDEventWorkspace* the the following happens:

```
def event_transform(ws, scale, offset):
  top_box = ws.get_box()
  boxes = top_box.get_boxes() # Get all leaf nodes
  for box in boxes:
    # Scale and shift the box extents for each dimension
    # and update the cached box volume.
    for dim in range(box.get_number_of_dimensions()):
      box.scale_and_shift_extents_for_dimension(dim, scale, offset)
      box.recalculate_volume()

    # Now we need to scale and shift the events inside the box too
    events = box.get_events()
    for event in events:
      for dim in range(box.get_number_of_dimensions()):
        event.centre[dim] = scale[dim]* event.centre[dim] + offset[dim]
```

###### Data Structure access
The same considerations regarding `getBoxes` apply as in other cases.

###### Comment on scalability and dependence on underlying data structure
This is a highly local operation and should in no scenario cause issues with
scalability, provided the underlying data structure allows easy local access (as
with all other algorithms).

### Utility
##### CloneMDWorkspace
This algorithm creates a copy of an existing workspace.

The *MDHistoWorkspace* essentially performs a `std::copy_n` of the signal,
error, event number and masking arrays. The *MDEventWorkspace* performs recursive
copying of the *MDBox* structure.

The scalability of this algorithm might be limited. While the new copies of the
data could be generated locally, it would be non-local to generate the underlying
connection to other data if it was stored in a hierarchical data structure.

##### CompareMDWorkspaces
For the *MDHistoWorkspace* a bin-by-bin comparison is performed. This is
possible locally.

For the *MDEventWorkspace* a box-by-box comparison of all (including internal) nodes
is performed. This is not locally possible with our hierarchical data structure.

### Other
* SaveMDWorkspaceToVTK
* ChangeQConvention
* QueryMDWorkspace
* SetMDFrame
