# Data structures which might lend them selves to the problem

### To Look at

* Distributed hashes
* B-tree
* R-tree
* kd-tree
* VDB
* AMR
* general space partitioning trees


## Distributed hashes

The key idea with a distributed hash is to split and map the key-space to
the participating nodes. The mapping of keys to nodes is normally achieved
by consistent hashing or rendezvous hashing. These schemes are minimally impacted
when changing the number of participating nodes.

### Pro
* Easy to implement
* Easy to scale
* Access and insertion is quick (however not clear what the key of event data would be)

### Con
* No inter
* No indexed access
* No co-locality and ranged access (but there are locality-sensitive hash functions;
  however this will bunch data onto few nodes)

Since we cannot perform any range queries, it is not clear how simple distributed
hash tables are of use to us at the moment.

TODO: Continue when appropriate
