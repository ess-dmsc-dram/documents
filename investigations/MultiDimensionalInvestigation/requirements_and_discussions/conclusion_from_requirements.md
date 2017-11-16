# Conclusion

This document summarizes the requirements and findings so far (end of week 4).

The groups which make use of multi-dimensional data structures can be classified
as variants of Single Crystal Diffraction and variants of inelastic direct. The
needs of these groups is very similar across facilities. One thing that is
common to all groups is the need to visually inspect the data, especially
in the *SliceViewer*

### Single Crystal Diffraction Requirements
Please see [here](./sumamry_of_workflows.md) for details of the work-flows of
the facilities. We have spoken with instrument scientists / lead developers for:
* WISH (ISIS)
* TOPAZ (SNS)
* NMX (ESS)
* MAGIC (ESS)  -- we are still talking to Xavier, but the information that we have
  so far indicates that he will operate in a similar manner to ISIS and the SNS.

#### Reduction

WISH, TOPAZ and MAGIC operate in a very similar manner. It can be broadly summarized as
1. Find peaks
2. Index peaks and obtain UB matrix
3. Integrate Peaks.
4. Centre the peaks.

This process is not necessarily linear and it can be that algorithms have to be rerun.
Often the *PeaksWorkspace* will be compared against the *MDEventWorkspace* in order
to check if peak-finding, peak-centering and peak refinement have worked well or
if the reduction parameters need to be tweaked. There are several algorithms which
operate on *MDEventWorkspace*, but there are alternatives in TOF:

|Q Space              | Altenative in TOF |
|---------------------|-------------------|
| *FindPeaksMD*       | *FindSXPeaks*|
| *IntegratePeaksMD*  | None yet, but can be rewritten to operate in TOF similar to *IntegrateEllipsoids*|
| *CentroidPeaksMD*   | *CentroidPeaks*|


This shows that the core algorithms which operate in reciprocal space have
alternatives in TOF (or at least it would be easy to write an alternative in TOF).

From our discussion with Esko we have learned that the reduction will take place
in TOF. A solution for the visualization needs to be provided which allows users to
inspect lambda-slices in detector space. The information that he provided suggests
that multi-dimensional data structures are not required for NMX.  

##### Visualization

Visualizations in Q space are integral for the data reduction. All instrument scientists /
 lead developers were quite adamant that the data reduction is quite an
iterative process that necessitates data inspection (especially via the *SliceViewer*).

Scientists often Zoom into their data. This means that data needs to be rebinned.
For this we require access to the underlying event information.

### Direct Inelastic Requirements
Please see [here](./sumamry_of_workflows.md) for details of the work-flows of
the facilities. We have spoken with instrument scientists / lead developers for:
* E.g. LET (ISIS)
* E.g. CNCS (SNS)
* CSPEC (ESS)

LET, CNCS and CSPEC operate in a fairly different manner. It can be broadly summarized as
1. Perform actual data reduction with *MatrixWorkspace*
2. Convert the all rotations to Q space and merge them
3. Perform further analysis

The second step is very different for the SNS and ISIS. It is not 100% clear,
how CSPEC will be operating. From some sample scripts it appears that the data
reduction will be similar to the SNS (which is however not surprising since the
sample data sets were collected at CNCS). The CSPEC instrument scientist has
mentioned though that we can use LET as an orientation. We are awaiting a definitive
decision between the two approaches.

#### Reduction scenario SNS

In this case *MDNormDirectSC* operates on an *MDEventWorkspace*. The first
step, however, is to convert the event-based workspace to a histogram-based
workspace. This means that *MDEventWorkspace* itself is not required and can be
taken out of the equation by:
1. Implementing *MatrixWorkspace*-to-*MDHistoWorkspace*-conversion in *ConvertToMD*
2. Make *MDNormDirectSC* accept *MDHistoWorkspace*

#### Reduction scenario 2

In this case we require *MDEventWorkspace*. The required algorithms are
1. *ConvertToMD*
2. *MergeMD*
3. Slicing (*SliceMD*)
4. Fitting with *Fit* and *FitResolutionConvolutionModel* (TobyFit)

This work-flow is currently performed in Horace and there is a serious initiative to
implement distributed support for Horace.

#### Visualization

Similar visualization requirements as in the SCD case apply here. We can
also consider to have a very finely gridded histogram-workspace which can be
then used for visualization (this depends on the required resolution and this
question is currently with the instrument scientist).

## Implementation options for multi-dimensional, even-based workspaces

The different approaches are explained for:
* [naive approach](../distributed_data_structures/naive_approach.md)
* [recursive coordinate bisection](../distributed_data_structures/recursive_coordinate_bisection.md)
* [space filling curves](../distributed_data_structures/space_filling_curves.md)

If we have to store an event-based structure to file for visualization we
would discard the "naive approach", since would have to combine the isolated
event-based structures on each node to a distributed event-based structure
anyway. There is nothing to be gained having two approaches.

## Recommendation

For Single Crystal Diffraction it looks like most of the required algorithms
can be pushed to TOF. Multi-dimensional data sets are only required for
visualization in the *SliceViewer*. The interactive reduction work-flow certainly
dominates here. This is problematic since we need to generate the multi-dimensional
data file (which can be consumed by the visualization client) every time the UB
matrix changes during the refinement process.

For the direct inelastic instruments, we will have to check what the outcome is
regarding the work-flow choice. In the best-case scenario we can avoid multi-dimensional
event-based scenarios entirely (for the data reduction). In the worst-case
scenario, we need to provide support for an event-based workspace which has a
small set of *MDAlgorithms* operating on it. The visualization will require
some sort of event-based workspace (this still needs to be confirmed by the
instrument scientist.)

The generation of a multi-dimensional, event-based workspace for visualization
seems to be very probable. The generation of the a distributed event-based
workspace would rely on established techniques such as recursive coordinate bisection (RCB)
or space filling curve traversal approaches. Having investigated both techniques,
it appears that the former(SFC) is conceptually simpler. However performance
comparisons seem give SFC a slight edge. See [here](https://www.sci.utah.edu/publications/SCITechReports/UUSCI-2008-006.pdf). Note
however that this will be highly problem and implementation dependent.
