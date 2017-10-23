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
structure is recursive as mentioned above.

TODO

## Creation

TODO


## Comments


TODO
