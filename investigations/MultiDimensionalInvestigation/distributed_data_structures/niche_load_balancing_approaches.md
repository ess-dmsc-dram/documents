# Space filling curve load balancing algorithms


The Zoltan library provides some niche algorithms which might be of interest to
us. The two approaches are Hilbert Space Filling Curve for (HSFC).
and Refinement Tree Partitioning

We only look at the HFSC method here. This algorithm is normally applied to octrees. A good description of the algorithm can be found [here](https://pdfs.semanticscholar.org/949f/0d4ea6d730f29aa11d42c061f3ddbd68888d.pdf)
Note that this algorithm will be able to produce a load-balanced distributed
data structure, but it does not seem to be immune to load spikes when
redistributing the data. This renders it not useful for our purposes.

Here we will only have a look at the parallel case, where we have p nodes and
a total of N data points. The steps are:
1. Every process access to a global octree which is generated up to a certain level.
   The level is determined by the number of participating nodes p. The level
   is Log(p)(note that the base is 8 for the octree), since we want one segment
   per node. Each global octant has a unique node as the owner. Only the terminal
   nodes of this global octree are required which stored in a map array. Each node knows which global octants are assigned to which process, in particular each node knows which
   octants are associated with it.
2. Every octant can hold M data points, before it needs to be refined (split).
   On each node we build up the local octree. Each node will have, in the homogeneous
   case N/p data points of which some are already in the right quadrant and other
   data points which are orphaned. For randomly distributed data we would
   expect the fraction of the data which is already on the correct node to be
   N/p. These data points need to be migrated to the correct processor and
   locally the octree construction is completed. **Note: At this point the
   algorithm stops being useful for us, since there is not guarantee that the
   data which is pushed to a node is less than what the node can handle**.
   We ignore this issue for now, since we might be able to circumvent this issue
   by creating the initial split via a sample set of the total data
3. Once the octree has been built, we need to calculate the prefix cost of the
   data. Note that this part is better explained [here](http://apps.fz-juelich.de/jsc-pubsystem/aigaion/attachments/SPartA_IPDPSW.pdf-299184f32c306328b4abeef3981a0075.pdf).
   The prefix cost is done locally on each node. We calculate this for every
   leaf node of the octree. The prefix cost for a given leaf node will depend
   on how we traverse the leaves. This is where space filling curves
   eventually come into play, but this can be separated out and we will look
   at this later.

   Besides calculating the local prefix costs we calculate the total cost per
   node (rank) which is communicated to the other nodes. From this we can
   calculate the total cost TC of all nodes and the prefix costs PC of the
   node(ranks) themselves. The nodes prefix cost offsets the prefix costs of
   the local leaves. This essentially establishes an ordering of leaves between
   nodes. The load balanced split is defined by OS = TC/p where p is the number of
   nodes. The splitting positions are defined by r*OS with 1<r<p. The local
   prefix costs (including the global offset of the rank) can be used to
   determine if a leaf is residing on the correct node or not. If it is not on the
   correct node, then we know from the split points and from its prefix to which
   node it should be mapped.
4. Sending the data to the correct node. In general the receiving node needs
   to be made aware that data will be sent. Depending on the tree, this set up
   will also require inter-node references, which looks not completely straightforward.


For the traversal of the leaves, several strategies can be applied. The Morton order
is very commonly used but suffers from fairly large jumps. Hilbert ordering
is more compute-intensive, but doesn't show the same jumping behaviour. However
it is more compute intensive.

#### n% approach

It is not very obvious that the n% sampling can be applied for this algorithm.
TODO
