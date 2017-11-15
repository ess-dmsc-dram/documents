# MDEventWorkspace

The *MDEventWorkspace* is used to store a collection of multi-dimensional events.
These multi-dimensional events are normally sparsely distributed in the parameter
space and hence an adaptive mesh refinement is used to store the data. Regions
with high signal density are more finely sampled than regions with low signal
density. This is a tree structure where leaf nodes are of type *MDBox* and
internal nodes are of type *MDGridBox*.

The multi-dimensional events (either *MDLeanEvent* or *MDEvent*) are the basic
unit of information and are always contained in the leaf nodes. If an *MDBox*
contains too many events (more than a set threshold) then the box is converted
to an *MDGridBox* with several *MDBox* es as leaves and the events are distributed
between them.

The image below should help to illustrate the data structure.
![MDEventWorkspace.](md_event_workspace.png)

## Structure

The *MDEventWorkspace* contains a pointer to an *MDBoxBase* object which is normally
an *MDGridBox* (if there are any events present in the workspace). From there the
structure is recursive as mentioned above. Another important element is the *BoxController*
which is shared between the *MDWorkspace* and all boxes. We will go through the
different components below.

### *MDGridBox*

The *MDGridBox* is the internal node type of the tree and never contains any events.
It contains links to a specified amount of child nodes which can be either of
type *MDGridBox* or of type *MDBox*. The total amount of children that the
*MDGridBox* will have depends on the number of splits per dimension which is
defined by the *BoxController*. The main methods are:
*  `TMDE(void MDGridBox)::splitAllIfNeeded(Kernel::ThreadScheduler *ts) ` and
`TMDE(MDGridBox)::MDGridBox(MDBox<MDE, nd> *box)` since they mainly drive the
splitting behaviour.
* `TMDE(inline size_t MDGridBox)::addEvent(const MDE &event)` since it is the
main way of growing the data structure.
* `TMDE(void MDGridBox)::getBoxes(std::vector<API::IMDNode *> &outBoxes, size_t maxDepth, bool leafOnly, Mantid::Geometry::MDImplicitFunction *function)`
  since it is the main way of accessing the underlying data.

Most other methods exist to support this core functionality. Exceptions to this
are some specialist methods such as `integrateSphere`, `integrateCylinder` and
`centroidSphere` which are used by several SCD algorithms.


##### The `splitAllIfNeeded` method

The method causes a recursive splitting of the data structure if the nodes contain
more events than what is specified in the *BoxController*. The method does:
```
def splitAllIfNeeded()
  for box in child_boxes:
    if box is MDBox:
      # 1. If we are dealing with an MDBox, then this contains data and might
      #    require a split
      if box_controller.should_split(box):
        new_box = new MDGridBox(box)
        replace box with new_box in child_boxes array
        new_box.splitAllIfNeeded()
    else:
      # 2. If we are dealing with an MDGridBox, then we have to check if its
      #    children need to be split.
      box.splitAllIfNeeded()
```

The children of the *MDGridBox* are recursively split if the box controller
determines that this is required. Note that the actual splitting occurs in the
constructor of *MDGridBox* which we describe below.

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

The method determines which child box an event needs to be added to via indexing.
Then the event is added to that box. Note that this might be recursive if the
target is an *MDGridBox*.

##### The `getBoxes` method

This method is the main way of accessing the underlying data. The user specifies
a maximum depth to search the tree, if only leaf nodes are relevant (which is mostly)
the case. She can provide an implicit function which will normally define
a ROI from which we want to retrieve boxes. Pointers to the boxes are added to an
output vector.

Assuming we are only interested in leaf nodes, the method of the *MDGridBox* can
be described as:
```
def getBoxes(output_boxes, max_depth, implicit_function)
if current_depth < max_depth:
  for box in child_boxes:
    # Check vertices if box is fully contained in volume defined by implicit function
    if implicit_function.is_fully contained(box):
      box.getBoxes(output_box, max_depth)
    elif implicit_function.is_touching(box):
      box.getBoxes(output_box, max_depth, implicit_function)
```

Recall that the *MDGridBox* is an internal node and in the pseudo-code above
we only want to retrieve leaf nodes, hence we don't see the box getting added
to the output.

The complexity here lies in determining if vertices are contained in the volume
which is defined by the implicit function and which are not. This requires
neighbour-vertex knowledge.

### *MDBox*

The box is similar to the *MDGridBox* (since both fullfill the *IMDNode* and
*MDBoxBase* contracts) but is mainly responsible for holding the actual
*MDEvents*. The events themselves are stored in a vector in no particular order.
The main methods have been described roughly above. The implementation will be of
course different since the actual data access is happening in the *MDBox*, but
conceptually it is the same.

### *BoxController*

The workspace contains a *BoxController* instance which is shared with
every *MDGridBox* and every *MDBox*. It contains information regarding splitting.
*MDGridBoxes* will check if a child is large enough to be split by querying the
*BoxController*. In addition it is used to keep track of the existing depth and
the number of boxes per level. As it stands, access to this object limits
scalability since updates to the number of boxes and tracking needs to happen
with a mutex of some kind.

### *MDBoxIterator*

A way to traverse the data structure is to use the *MDBoxIterator*. When
this is constructed it creates a vector of pointers to all (leaf) nodes and
then iterates through this vector. Populating this vector uses `getBoxes` and
since this uses a depth-first approach the leaves are traversed in this manner.

## Creation

The main algorithm for the creation of multi-dimensional workspaces is
*ConvertToMD* which takes a *MatrixWorkspace* and produces an *MDEventWorkspace*.
This algorithm is general purpose and used for a wide range of groups.
It is also quite complex. To get an understanding about the formation of an
*MDEventWorkspace*, please see [here](../algorithm_categorization/pure_event_algorithm_description.md)

## File-backed operation

File-backed operation of some MD workspaces is required when dealing with data which
is too large to fit into memory. A file-backed *MDEventWorkspace* will have a link to
a file where data is stored. This feature is quite complex and we need to discuss if
this is required (and how this will fit into distributed loading).

TODO: Investigate more?

## Comments on scalability

* Scalability of the splitting behaviour: This is a local operation which does
not affect boxes in other branches. However, depending on the implementation,
we might have to reshuffle boxes to other nodes.

* Scalability of growing the structure: If the underlying data structure
supports memory locality of co-located events, then it should be possible to add
events in a distributed/scalable manner (e.g. if we were dealing with a distributed
locality-sensitive hash table). However, after a while events might have to be
rebalanced between ranks since the data is highly sparse, e.g.SCD.

* Scalability of data access: Most access is either a query for all leaf nodes
  or for all leaf nodes in a sub-volume defined by an implicit function.
  Again if the underlying structure supports memory locality of co-located events
  (e.g. which belong to the same peak), then it is thinkable to efficiently
  retrieve that data.
