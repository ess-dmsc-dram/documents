# Recursive Coordinate Bisection

Recursive Coordinate Bisection (RCB) is a standard algorithm for load balancing
spatial data in numerical simulations across a range of processes. This is
essentially the algorithm which is used by *VTK* and *ParaView* to distribute
data between nodes using the *vtkDistributedDataFilter*. The algorithm is
reasonably simple (at least conceptually) and essentially just builds up a
kd-tree. Load-balancing the data between the nodes means to build a kd-tree up to
level of Log(p), where p is the number of participating nodes.

There are other load-balancing algorithms, but this seems to be a widely
used algorithm which has been around for a long time. A dedicated load-balancing
library which offers this algorithm for load-balancing is [Zoltan](http://www.cs.sandia.gov/zoltan/).
Unfortunately, this library is aimed at 1D-3D data structures, hence it is
not quite suitable for us. Nevertheless, this can serve as a good reference, since
it contains a range of different load-balancing options.
We should also consider:
* Recursive Inertial Bisection
* Hilbert Space-Filing Curve Partitioning
* Refinement Tree Based Partitioning

### Algorithm

One of the most insightful papers on the subject is ["Parallel Construction of Multidimensional
Binary SearchTrees"](http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.96.6065&rep=rep1&type=pdf).
We will use the algorithm description from there. There are variations to this algorithm, but the median-based method seems to provide the best performance.

#### Median-based method

The general work-flow of the algorithm for N data points and p nodes is relatively simple.
We focus here on the parallel construction of a kd-tree up to level Log(p). It
can be described as:
1. Choose a split direction for the region under investigation, e.g. of longest elongation of  
   the current region.
2. Find the median element of the data points (in the current region) along that direction.
   This means we are dealing with data points across several nodes, hence we
   require a parallel median finding algorithm.
3. Partition the data based on the median that was calculated in step 2. Each node
   will locally split its data points into a group that is either below or above
   the median. All points less or equal to the median are transferred to nodes P(1), P(2), ...P(p/2-1) and the other points to P(p/2), ...P(p). Note that this labelling scheme is
   only correct for the outermost region. The labelling changes when we are at split levels > 0.
4. Apply steps 1 through 3 until on the two sub-regions until we have p sub-regions, i.e. until
   the kd-tree has reached a depth of Log(p), which is only nicely achievable if p is a power of 2.
5. Arrange the data in the required format, e.g. continue building the kd-tree locally.

The difficult part of the algorithm is to find the median of all data points. Deterministic
median-finding algorithms don't perform well if the data is not randomly distributed, hence
a randomized algorithm is suggested (this might require randomization of the data on the
N nodes). Several parallel selection algorithms are discussed [here](https://surface.syr.edu/cgi/viewcontent.cgi?referer=https://www.google.co.uk/&httpsredir=1&article=1028&context=lcsmith_other). Specifically the Floyd-Rivest algorithm is suggested.

With the approach described above, we have a lot of data movement. The paper suggests to
cache the splits locally on each node. This means that each node has a part of each partition. This increases the communication for median finding but the transport of the actual data can be postponed until p regions have been established. After the regions have been established, data from each node is sent to the correct receiver.

### Final data structure

The above describes only the partition scheme onto the different nodes. On the nodes
we can either continue to use a kd-tree (as is done in VTK) or we use our own
data structure. Using an adaptive mesh refinement as we are currently doing should
have the least impact on the current implementations of the algorithms.

In order to understand the costs of the operations better we should run through
some typical operations that we might perform on the distributed data structure.
We will briefly look at Q space conversion and *IntegratePeaksMD*. In addition
we want to have a look how we could visualize the data.

#### Creation

1. The raw event data is converted to Q space on each node. This is a runtime cost of O[N/p].
2. The data is split in a load-balanced manner. Overall this depends on the
   data distribution. In the case of randomly distributed data, the above
   paper suggests that the complexity of the computation can be O[N/p(Log(p))]
   and the complexity of the data transfer can be O[N/p].
3. Each node should have N/p data points. Now we build the local data structure,
   where we can estimate an upper bound of tree creation in the case of
   homogeneous data. We can say that we place N/p events into a tree of depth
   Log(N/p). Hence, O[N/p\*Log(N/p)] should be a reasonable estimate.

Note that the naive approach where we have a separate event workspace which
spans the full Q space on each node would result in trees which are slightly
deeper. However, since the first split is often something like 50 per
dimension we should have a top-level splitting which is comparable with the
partition that we get when we distribute the data across ranks.

#### Using the distributed data structure for spherical peak integration.

Peak integration has one of its main algorithms operating in Q space, *IntegratePeaksMD*.
This algorithm is described [here](../algorithm_categorization/pure_event_algorithm_description.md)

The algorithm will take a peak position, radius and background radius as inputs
(which it gets from the *PeaksWorkspace*). The algorithm calls `integreateSphere`
on the top level box.  The `integreateSphere` method iterates over all child boxes and checks if their vertices are fully or partially contained in the integration region. If the box is fully contained in the integration region, then the box's signal is added to the integrated signal; if the box contributes partially, then the child box is recursively investigated.

This needs and can be performed on all nodes separately. Each node will hold its own
signal contribution which needs to be gathered and summed up on the master rank.

The naive approach operates in exactly the same way. It is not obvious that the
complexity of the naive approach is worse than in the space-partitioned
approach.

##### Visualizing data

We will have to support some form of data inspection, e.g. via the *SliceViewer*.
Since one of the key requirements there is to be able to zoom into the data sets
in order to determine how well peak integration and/or finding has worked, we will
have to provide access to the *MDEventWorkspace*. Loading a full *MDEventWorkspace*
into memory might be out of the question, but this needs to be confirmed. One way
to still use an *MDEventWorkspace* is to operate in the file-baked mode. Here the
main boxes can fetch event information from the disk and free up that memory when
it is no longer required. The main algorithm for the visualization is *BinMD*
which will generate the slice for us. To build up the signal in the bins, the
*MDEventWorkspace* will most likely have to fetch data from the disk.

The kd-tree partitioned data set should be fairly easy to save to file in way
that ensures that co-located data is saved close to each other on file. We would
have to consider that the data structure looks and behaves quite differently up
to the node/process level where we have the kd-tree structure. The splitting
behaviour is completely different to what we use for the standard box structures,
i.e. each split is performed only in one geometric dimension, we split only in
half and the split is not even. To mitigate this we could introduce a third type
of box which is adapted to the distributed structure. In addition we would have
to teach the *BoxController* about this third box type. One down side with
saving the workspace out like this is potentially the fact that we are imprinting
the number of nodes that were processing the data at the time of creation. If
we reload that data set to a cluster with fewer nodes, then the data structure
will not map nicely to it.

In the naive approach we would essentially have to save out p workspaces to file,
albeit grouped. This would mean that we have to query data for the same Q region
from p locations in the file (can we have parallel reading?). This might be considerably
worse performance-wise.   

### Version with sampling

Simon suggested to improve the partitioning of the data by determining the regions
which are available on each node via a small sample of data from a couple of frames.
Each frame is a small shot of neutrons onto the sample which already represents
the correct distribution of scattering events on the detector bank. The signal
to background noise ratio from a single frame however is not very good, hence
many frames are added to improve the statistics. This means that with part of
the data it should be possible to estimate the Q-space distribution of data.
The idea is to only look at a fraction f of the total collected frames. This
would provide a considerable speed up when determining the
regions which should be associated with each node. Essentially the complexity
analysis above would replace N with N\*f.

It should be noted that there are also extra costs which we need to have a look at:
1. Determining the events which participate in a sample.
2. Transfer of the remaining N\*(1-f) events.

#### Sample selection

We want to select a fraction f of the data which is large enough such that we
can expect to see features. This might be instrument and sample dependent in which
case setting the fraction f of the total data might have to be adjusted. Note that
setting f=1 will nicely transition into the unoptimized case.

When the data is loaded into the *MatrixWorkspace* the event lists will contain
the events ordered by increasing pulse time. The way to get the fraction f of events is:
1. Get start and end time from the sample logs, i.e. query `start_time` and `end_time`
2. Get the cut-off pulse time to obtain the fraction f: cut_off_time = start_time + f\*(end_time-start_time).
3. For each event list find the index in the event list where the pulse time
   of the event is smaller or equal to the cut off time calculated in step 2.
From this we can get a sample with which we can build the regions.

The main difficulty lies in finding the indices in the spectra. If we have M spectra,
then we can estimate that each spectrum has N/M events and each node will have
M/p spectra. Finding the index is a simple bisection algorithm. The complexity of
this will be O[M/p\*Log(N/M)].

#### Transfer of the remaining data

Once we have set up the regions on the p nodes we need to transfer the remaining
(1-f)\*N data points. Each event needs to go down the kd-tree to find its correct region/node. This should be O[Log(p)]. However, I assume we can optimize this to O[1] (we do something
similar for the current boxes). We have (1-f)\*N/p events to send per node. This
means that we should end up with O[(1-f)\*N/p]\*(or O[(1-f)\*N/p*Log(p)]) transfers.

#### Comparison of the creation with the standard approach

The only part where the two approaches differ is in the way load-balancing is
performed. Recall that the complexity of the calculation was O[N/p(k+Log(p))] and the
complexity of the transfer was O[k\*N/p] for the standard approach according to
the above publication.

The sampled approach will have O[f\*N/p(Log(p))] for the computation and O[f\*N/p]
for the region-building step. Adding the final transfer step leads to O[N/p].

This clearly shows that with the sampling approach we don't really change the
complexity, but certainly the scaling factor (considerably) for the median
calculation. This is of course only possible since we make certain assumptions
regarding the data. If the sample is not representative of the total distribution
of events, then we could end up with a heavily unbalanced spatial partitioning.
How well this performs needs to be established experimentally.
