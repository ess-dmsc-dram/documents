# LocalMap-Reduce

A simple way of performing a conversions to the MD domain is by mapping the spectra
on each rank into a local MD data structure. Operations are performed locally.
The data is then finally reduced onto a single rank where it is converted into
an *MDHistoWorkspace*.

The benefits of this approach are clear. It is by far the simplest imoplementation
since it can reuse the data structures which we already have. In addition, this
apprach does not require an initial redistribution of data between ranks.

### Concerns

There are several concerns and limiations regarding this approach:
* The partioning does not scale in terms of workload
* The *FindPeaksMD* algorithm will not work in this configuration, at least not
  easily

##### Investigation of these concerns

###### Performance scaling concern

The concern that was raised, is that in this scheme the processing of the data
set might take the same time regardless if the data is being partioned or not.
Let' say we have N events and R ranks. The analysis here is only concerned with
events and we assume that the loads are balanced (if this is not the case, then
we have the same issus for the standard *MatrixWorkspace*)

The approach contains several components:
1. Mapping from events to MDEvents: O(N/R)
2. Operation: ???
3. Reduction onto a single rank: O(N)

Clearly, we have to go through each algorithm to check in 2) how the algorithm
would scale. From our previous analysis we know that most algorithms access
the workspace via only a few methods. These are:
* `addEvent`: Since we have N/R events on each rank we would have a complexity O(N/R) provided we accessed all events (which is mostly the case). An example of this would be *PlusMD*.
* `getBoxes`: In most cases we use this method in order to retrieve leaf nodes, either
all of them or only the ones which are within a volume specfied by an implicit function.
All boxes are touched normally in this operation. In the case of a homogenous distribution
this would 


###### FindPeaksMD concern

The algorihtm as we know it will now work, since it is a non-local algorihtm
which compares all boxes with each other. However there is a good chanc that this
will also not work for implementations which make use of other data structures,
since this algorithm only works because of its knowledge of the underlying
implementation.

Also, the *FindPeaksMD* has not been performing well. Scientists at ISIS have
moved to the TOF domain to perform peak searching. However, if *FindPeaksMD*
is strongly required, we could transform an event-type workspace to a
*MDHistoWorkspace* and apply the algorithm to it.


### Typical workflows in this configuration

Here we want to discuss the typical workflows that might use MD data structures
and algorithms and see how they would behave in this configuration.

#### Single Crystal diffraction

##### Typical workflow

##### In this realisation

#### Diffuse Scattering

##### Typical workflow

##### In this realisation

#### Inelastic workflow

##### Typical workflow

##### In this realisation
