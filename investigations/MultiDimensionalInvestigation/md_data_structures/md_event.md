# MDEventWorkspace

The *MDEventWorkspace* is considerably more complex than the *MDHistoWorkspace*.
This workspace type has a tree structure where leaf nodes are of type *MDBox*
and internal nodes are of type *MDGridBox*.  The multidimensional events
(either *MDLeanEvent* or *MDEvent*) elements are the basic unit of information and
are always contained in the leaf nodes. If an *MDBox* contains too many events (more
than a set threshold) then the box is converts itself to an *MDGridBox* with several *MDBox* es
as leaves and the events and distributes the  between them. This is essentially an adaptive
mesh refinement technique. This ensures that areas with a high density of information
are more finely sampled than areas with a low density.

The image below should clarify the situation.
![MDEventWorkspace.](md_event_workspace.png)

## Structure

The *MDEventWorkspace* contains a pointer to an *MDBoxBase* object which is normally
an *MDGridBox* if there are any events present in the workspace. From there the
structure is recursive as mentioned above. Another important element is the *BoxController*
which is shared between the *MDWorkspace* and all boxes. We will go through the
different components below now.

### *MDGridBox*

The *MDGridBox* is an internal node in the tree and never holds any data it has
a certain amount of child nodes which can be either of type *MDGridBox* or of type
*MDBox*. The total amount of children that the *MDGridBox* will have depends on
the number of splits per dimension which is defined by the BoxController. The
main methods are:
*  `TMDE(void MDGridBox)::splitAllIfNeeded(Kernel::ThreadScheduler *ts) ` and
`TMDE(MDGridBox)::MDGridBox(MDBox<MDE, nd> *box)` since they mainly drive the
splitting behaviour
* `TMDE(inline size_t MDGridBox)::addEvent(const MDE &event)` since it is the
main way of growing the data structure
* `TMDE(void MDGridBox)::getBoxes(std::vector<API::IMDNode *> &outBoxes, size_t maxDepth, bool leafOnly, Mantid::Geometry::MDImplicitFunction *function)`
  since it is the main way of accessing the underlying data.

Most other methods exist to support this core functionality. Exceptions to this
are some specialist methods such as `integrateSphere`, `integrateCylinder` and
`centroidSphere` which are used by several SCD algorithms.


##### The `splitAllIfNeeded` method

The method does:
```
def splitAllIfNeeded()
  for box in child_boxes:
    if box is MDBox:
      if box_controller.should_split(box):
        new_box = new MDGridBox(box)
        replace box with new_box in child_boxes array
        new_box.splitAllIfNeeded()
    else:
      box.splitAllIfNeeded()
```

The children of the *MDGridBox* are recursively split if the box controller
determines that this is required. Note that the actuall splitting occurs in the
contructor of *MDGridBox* which we describe below.

##### The `MDGridBox` constructor

This constructor takes an *MDBox* instance which has grown to large and distributes
its events to a bunch of child *MDBox* instances of the newly created *MDGridBox*.
The functional flow is
1. Create n child *MDBox* instances and set the *MDGridBox* as the parent. Also set
   extents etc.
1. For each event in the box add the event to the *MDGridBox* (this will percolate to the)
   appropriate *MDBox*
1. Clear the input *MDBox* (note that the box is deleted in the `splitAllIfNeeded` method)

##### The `addEvent` method

The method determines which child box the event needs to be added to via indexing.
Then the event is added to that box. Note that this might be recursive.

##### The `getBoxes` method

This method is the main way of accessing the underlying data. The user specifies
a maximum depth to search the tree, if only leaf nodes are relevant (which is mostly)
the case and she can provide an implicit function which will normally define
a region of interest from which we want to retrieve boxes. Pointeres to the boxes
are added to an output vector.

Assuming we are only interested in leaf nodes, the algorihtm can be described as:
```
def getBoxes(output_box, max_depth, implicit_function)
if current_depth < max_depth:
  for box in child_boxes:
    check vertices if box is fully contained in volume defined by implicit function
    if is fully contained:
      call box.getBoxes(output_box, max_depth) # Note without the implicit function
    elif is touching:
      call box.getBoxes(output_box, max_depth, implicit_function)
```

The complexity here lies in determining if vertices are contained in the volume
which is defined by the volume and which are not. This requires neighbour-vertex
knowledge.

### *MDBox*

The box is similar to the *MDGridBox* (since both fullfil the *IMDNode* and *MDBoxBase* contracts) but is mainly responsible for holding the actual *MDEvents*. The events
themselves are stored in the vector in no particular order in the box.
The main methods have been decribed roughly above. The implementation will be of
course different since the actual data access is happening in the *MDBox*, but
conceptually it is the same.

### *BoxController*

The workspace contains a *BoxController* instance which is shared with
every *MDGridBox* and every *MDBox*. It contains information regarding splitting.
*MDGridBoxes* will check if a child is large enough to be split by querying the
*BoxController*. In addition it is used to keep track of the existing depth and
the number of boxes per level. As it stands access to this object limit scalability
since updates to the number of boxes tracking need to happen with a mutex of
some kind.

### *MDBoxIterator*

A comon way to traverse the data structure is to use the *MDBoxIterator*. When
this is constructed it creates a vector of pointers to all (leaf) nodes and
then iterates through this vector. Populating this vector uses `getBoxes` and
since this uses a deapth-first approach the leafes are traversed in this manner.

## Creation

The main algorithm for the creation of MDWorkspaces is ConvertToMD which takes
a MatrixWorkspace and produces an MDEventWorkspace. This algorithm is general
purpose for a wide range of groups. It is also very complex and badly documented,
hence we focus on an algorithm which is not used any longer but conveys the intent
of the MD creation better -- the first version of *ConvertToDiffractionMDWorkspace*

### ConvertToDiffractionMDWorkspace

The algorihtm can operate on operate on `Workspace2D` and `EventWorkspace`. It
takes into account the frame into which we want to convert, ie `QLab`, `QSample`
 or `HKL`. Note that `Workspace2D` spectra are converted to event lists with weighted
 events. The events in the event lists are added to an empty `MDEventWorkspace`
 in the following manner:

 ```
def convert_event(event, md_event_ws, spectrum_info, workspace_index, rotation_matrix):
  box = md_event_ws.getBox()

  # Get Q direction in lab frame
  detector_position = spectrum_info.position(workspace_index)
  detector_direction = detector_position / detector_position.norm()
  beam_direction = get_direction()

  q_direction_lab_frame = detector_direction - beam_direction

  # Get Q direction in desired frame
  q_direction = rotation_matrix*q_direction_lab_frame

  # Gather constants
  wavenumber_in_angstrom_times_tof_in_microsec = neutron_mass * distance * 1e-10 / (1e-6*hbar)

  wavenumber = wavenumber_in_angstrom_times_tof_in_microsec / event.tof()
  q_center = q_direction * wavenumber

  if is_within_extents(q_center):
    box.add_event(MDEvent(box.weight), box.error_squared, q_center)
 ```

Note that this ignores several things, e.g, LorentzCorrection.

## File-backed operation

File-backed operation of some MD workspaces is required when dealing with data which
is too large to fit into memory. A file-backed MDEventWorkspace will have handle to
a file where data is stored. This feature is quite complex and we need to discuss if
this is required (and how this will fit into distributed loading).

TODO: Investigat more?

## Comments to scalability

* Scalability of the splitting behaviour: The splitting is behaviour is a local
operation which does not affect boxes in other branches.

* Scalability of growing structure: If the underlying data structure
supports memory locality of colocated events, then it should be possible have
events parallelizable. However, after a while events might have to be rebalanced between
ranks since the data is highly sparse (for SCD).

* Scalability of data access: Often access to the boxes is concerned to a region
of interest in q space which is defined by an implicit function. If the underlying
structre supports memory locality of colocated events (e.g. which belong to the same peak),
then for these scenarios only a part of the data structure needs to be targeted.
