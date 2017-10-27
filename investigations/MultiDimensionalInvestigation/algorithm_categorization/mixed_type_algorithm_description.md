# Description of pure mixed type algorithms

In this document we want to describe MDAlgorithms which  operate on
event-type and histogram-type workspaces. It is not intention to give an
algorithmically exact representation of the algorithms but rather to get a good
understanding of their functionality and their dependence on
data-structure-specific features.


## Mixed algorithms
### Creation
* SaveMD
* LoadMD

### MDArithmetic
#### MinusMD

The *MinusMD* algorithm is used to subtract two workspaces.

###### Execution

In the case of *MDHistoWorkspace* subtraction the binning and dimensionality
needs match between the two workspaces. The signals of the two workspaces are
subtracted from each other and the squared errors are added.

In the case of *MDEventWorkspace* subtraction, the worflow below is used:

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

### PlusMD
This is the same as *MinusMD*, but we don't use the inversion of the signal value.
The same considerations regarding the scalability apply here.

* BinaryOperationMD (Base algorithm)
* UnaryOperationMD (Base algorithm for which the derived algorithms only work on MDHisto. Why accept both then?)

### Peaks
### FindPeaksMD
TODO


* IntegratePeaksMDHKL

### Slicing
##### BinMD (but histogram needs link to original event or weighted workspace)
TODO
* CutMD (forwarding algorithm)

### Transforms
#### MaskMD
The algorithm masks all data in a rectangular block on an MDWorkspace.

###### Execution
The user specifies extents in the dimensions she wants to apply masking. Several
boxs can be specified. The box specifications are grouped on a per-box basis.
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
It caontsais the same constraints as other algorithms that use `getBoxes`, e.g. *MinusMD*.

#### TransformMD
This algorihtm provides a lienar transformation, ie offset and scale for each
dimension in an *MDWorkspace*.

###### Execution
The algorithm changes the relevant entries in the *MDHistoDimension* of the workspace.

If the algorithm is an *MDHistoWorkspace*, then there is nothing left todo, unless
the scaling was negative in which case the raw signal array is inverted. This could
be an issue if we wanted to have a distributed *MDHistoWorkspace*, but that
would depend on the implmentation details.

If the algorihtm is an *MDEventWorkspace* the the following happens:

```
def event_transform(ws, scale, offset):
  top_box = ws.get_box()
  boxes = top_box.get_boxes() # Get all leaf nodes
  for box in boxes:
    # Scale and shift the box extents for each dimension
    # and update the cached box volume.
    for dim in box.get_number_of_dimensions():
      box.scale_and_shift_extents_for_dimension(dim, scale, offset)
      box.recalculate_volume()

    # Now we need to scale and shift the events inside the box too
    events = box.get_events()
    for event in events:
      for dim in box.get_number_of_dimensions()
        event.centre[dim] = scale[dim]* event.centre[dim] + offset[dim]
```

###### Data Structure access
The same considerations regarding `getBoxes` apply as in other cases.

###### Comment on scalability and dependence on underlying data structure
This is a highly local operation and should in no scenario cause issues with
scalability, provided the underlying data structure allows easy local access (as
with all other algorithms).

### Utility
* CloneMDWorkspace
* CompareMDWorkspaces

### Other
* SaveMDWorkspaceToVTK
* ChangeQConvention
* QueryMDWorkspace
* SetMDFrame
