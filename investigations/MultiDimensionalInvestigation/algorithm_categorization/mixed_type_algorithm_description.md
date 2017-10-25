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
### BinMD (but histogram needs link to original event or weighted workspace)
TODO
* CutMD (forwarding algorithm)

### Transforms
* MaskMD
* TransformMD

### Utility
* CloneMDWorkspace
* CompareMDWorkspaces

### Other
* SaveMDWorkspaceToVTK
* ChangeQConvention
* QueryMDWorkspace
* SetMDFrame
