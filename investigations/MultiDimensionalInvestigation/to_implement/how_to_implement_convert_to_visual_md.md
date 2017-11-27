# How to implement a distributed ConvertToVisualMD

The implementation instructions are based on this [document](../distributed_data_structures/simon_split.md), but provide a
much more detailed description and full design of the feature.


The components and pieces of work of the algorithm are:
* Momentum transfer converter
* n%-sampler
* tree-splitter
* tree-split-assigner
* tree-skeleton serializer
* tree-sekelton communicator
* event distributer
* local-tree ammender
* data

### Momentum transfer converter

Getting this right might take a while since it is based on *ConvertToQ*. However
a basic implementation of this is sufficient for the
