# MDHistoWorkspace

The *MDHistoWorkspace* is in principal a regular n-dimensional grid. Most often
it will be either three- or four dimensional. Each element of the grid is a
hyperrectangle of equal size. Note that the extents along the individual dimensions
does not have to be equal.

## Structure

The *MDHistoWorkspace* saves information about the signal of each bin, the
error-squared in each bin, the number of contributing events in each bin.
Additionally, it stores information about the dimensionality, the overall extent,
the extent of a single box, etc. The signal/error/event data comprises the bulk
of the information stored in the *MDHistoWorkspace*. This data is stored in
a dynamically allocated linear array. The linear array can be easily mapped
into multiple dimensions, ie multi-dimensional indexing is easily possible.
In addition a vertex array is stored. This is the collection of coordinates
of vertices which make the 0th box. This is important when calculating slices
through the MDWorkspace of if a box is partially, fully or not contained inside
a volume.

## Creation

There are several ways to create an *MDHistoWorkspace*. The most common are:
1. **Via slicing**: The *BinMD* and algorithm allows for transforming an *MDEventWorkspace*
into an *MDHistoWorkspace*. The algorithm properties determine the bin sizes and
the events are then added into the correct bins.
1. **Via file loading**: The algorithms which can load saved data into an *MDHistoWorkspace* are
  * ImportMDHistoWorkspace
  * LoadMD (this also works for *MDEventWorkspace*)
1. **Via conversion from a *MatrixWorkspace***: The main algorithm here is *ConvertToReflectometryQ*.
1. **Via direct creation**: By providing signal and error arrays it is possible to directly
create an *MDHistoWorkspace* using *CreateMDHistoWorkspace*.

## Comments

The size of the *MDHistoWorkspace* is neither determined by the number of underlying
events that have contributed to the data nor by the number of detectors. It's
size is essentially governed by the dimensionality, the binning and the extents
of the Q-space region that the user is interested in.

Note that the majority of the arithmetic algorithms are only defined on this type
of workspace.
