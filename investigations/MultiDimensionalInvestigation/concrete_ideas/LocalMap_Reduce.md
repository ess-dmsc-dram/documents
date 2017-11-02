# LocalMap-Reduce

A simple way of performing a conversions to the MD domain is by mapping the spectra
on each rank into a local MD data structure. Operations are performed locally.
The data is then finally reduced onto a single rank where it is converted into
an *MDHistoWorkspace* (on the fly).

The benefits of this approach are clear. It is by far the simplest implementation
since it can reuse the data structures which we already have. In addition, this
approach does not require an initial redistribution of data between ranks.

### Concerns

There are several concerns and limitations regarding this approach:
* The partitioning does not scale with the workload (at least not trivially)
* The *FindPeaksMD* algorithm will not work in this configuration

##### Investigation of these concerns

###### Performance scaling concern

The concern that processing the data in this way might take the same time
regardless if the data is being partitioned or not. Let' say we have N events
and R ranks. The analysis here is only concerned with events and we assume that
the loads are balanced (if this is not the case, then we have the same issues
for the standard *MatrixWorkspace*)

The approach contains several components:
1. Mapping from events to *MDEvents*: O(N/R)
2. Operation: ???
3. Reduction onto a single rank: O(N)

Clearly, we have to go through each algorithm to check in 2) how the algorithm
would scale. From our previous analysis we know that most algorithms access
the workspace via only a few methods. These are:
* `addEvent`: We have N/R events on each rank. If we assume that the tree structure
is not vastly different on a partitioned data set or a single full data set, then
we get a tree of height Log(N). This means to place the N/R events into the
data structure we would have O(N/R*Log(N)) operations.
* `getBoxes`: In most cases we use this method in order to retrieve leaf nodes, either
all of them or only the ones which are within a volume specified by an implicit function.
There is definitely no guaranteed scaling in this operation. Distributing the
events can remove one or several levels of the tree however, which will have a (potentially very large) performance improvement. However this depends strongly on the split parameters, the number of ranks and the number and distribution of events. As such we should
assume that this operation does not scale. It is not clear that this is
a bad result however, since we are essentially dealing with workspaces of the
size we are used to at ISIS or the SNS (per machine). As part of the `getBoxes`
call we are often dealing with accessing the underlying events. In the evenly
distributed scenario (which is unrealistic) this would again have a complexity of O(N/R* Log(N)).  
* `splitAllIfNeeded`: This traverses the entire tree. Hence the same considerations
  as with `getBoxes` apply here.

In summary: Many parts of this approach scale linearly with the number of machines
that are used to solve this problem. However the tree traversal does not scale in the
same manner. This might not really be a too big issue since we would be dealing
with a processing time which is given by a workspace with N/R events on a single machine.

###### FindPeaksMD concern

The algorithm as we know it will not work, since it is a non-local algorithm
which compares all boxes with each other (sorting and box rejection). However
there is a good  chance that this will also not work for implementations which
make use of other data structures, since this algorithm only works because of
its knowledge of data structure implementation details.

Also, the *FindPeaksMD* has not been performing well. Scientists at ISIS have
moved to the TOF domain to perform peak searching. However, if *FindPeaksMD*
is strongly required, we could transform an event-type workspace to a
*MDHistoWorkspace* and apply the algorithm to it.

### Typical work-flows in this configuration

Here we want to discuss the typical work-flows that might use MD data structures
and algorithms and see how they would behave in this configuration.

#### Single Crystal diffraction

##### Typical workflow

The typical SCD work-flow at ISIS is:
* Perform preprocessing on *MatrixWorkspace* (e.g. setting UB Matrix, finding peaks)
* Run *ConvertToMD* to obtain an *MDEventWorkspace*
* Used to run *FindPeaksMD*
* Run *IntegratePeaksMD*
* Run *CentroidPeaksMD* (this can also be done in time-of-flight soon)
* Look at slices using *BinMD* (not applicable for us)

##### In this realisation

* After the preprocessing, we run *ConvertToMD*: The algorithm mainly calls `addEvent`
  with complexity O(N/R*Log(N)) and `splitAllIfNeeded` which has a complexity which
  is data set dependent.
* As explained above, this approach cannot use *FindPeaksMD*. However there are alternative
approaches which seem to operate adequately in time-of-flight.
* Then we run the *IntegratePeaksMD* algorithm: This relies on calling `integrateSphere` which in turn iterates over all boxes. Hence we have again a complexity that is data set dependent.
* Then we might run *CentroidPeaksMD*: This relies on calling `centroidSphere` which in turn
iterates over all boxes. Hence we have again a complexity that is data set dependent.

#### Inelastic workflow

##### Typical workflow

There are several approaches. At ISIS the workflow is:

* Perform preprocessing on *MatrixWorkspace*
* Run *ConvertToMD* to obtain an *MDEventWorkspace* for several workspaces
* Run *MergeMD*
* Then *Fit* and *FitResolutionConvolvedModel* are used

##### In this realisation

TODO: Check with others if this is something to pursue
