# Work items

The difficulty of the work items is assessed on a scale from 1 to 10 where
1 is the easiest.

## Distributed work

### ConvertToMDHisto

We need an algorithm which converts the distributed *EventWorkspace* into
a *MDHistoWorkspace* which can be held on a single machine. This would then
be used as the input for the normalziation algorithms. A detailed explanation
how to build this is presented [here](./how_to_implement_convert_to_md_histo.md).

Difficulty: 8

Time estimate: The main difficulty is porting the functionality from
               *ConvertToMD* to this algorithm. The estimate is 2 to 4 months.

### Write ConvertToMDVisualEventWorkspace (based on ConvertToMD)

Create an algorithm which converts a distributed *EventWorkspace* to a
distributed *MDEventWorkspace*. The approach for how to create it is described
in detail [here](../distributed_data_structures/simon_split.md). Once the
distributed *MDEventWorkspace* has been created, it can be saved with a
distributed *SaveMD* algorithm.

Difficulty: 10+

Time estimate: There are several levels of difficulty here.
1. The MPI part, e.g. load balancing
2. Porting *ConvertToMD* functionality
3. Validation

  The first part is estimated to be 3 to 6 months. The second part is estimated to be 2 to 4 months. The third part is estimated to be 1 month. This adds up to 6 to 11 months.

### Create a distributed SaveMD

We need to ensure that saving does not go through only a single rank, but that
we can do this entirely in parallel on a distributed *MDEventWorkspace*. This
should be possible as outlined at the end of
 [this](../distributed_data_structures/simon_split.md) document.

Difficulty: 9

Time estimate: Parallel writing should be possible, but is an unknown
               and we could expect 2 to 6 months.

## Mantid enhancement

### Alternative input for MDNormSCD adn MDNormDirectSC
These algorithms take an `MDEventWorkspace` as the input but convert it
directly to `MDHistoWorkspace`. We have to allow for a direct input of `MDEventWorkspace`
into these two algorithms.

Difficulty: 1
Time estimate: Since we only forsee to change the algorithm to accept *MDHistoWorkspace*,
               we expect the time to be little. The estimate is between 1 to 2 days.

### Spherical peak integration in TOF
*IntegratePeaksMD* is the main algorithm for spherical peak integration,
but it operates in Q space. We can port this to TOF. No direct instructions are
provided since will mainly have to copy the mechanism established in
*IntegreateEllipsoids*.

Difficulty: 4

Time estimate: We have something similar already in place for elliptical peaks. However comparing the new algorithm results with the old one might take some extra time. The estimate is between 2 to 4 weeks.

## Peformance optimizations

### Improve performance of BinMD for non-MPI builds
Since *BinMD* is used for the visualization, we will have to make it as
fast as possible. Currently it does not support parallel processing when using
file-backed data. See [here](../how_to_make_bin_md_parallel_for_file_backed.md)
for instructions.

Difficulty: 7

Time estimate: It is not clear that the suggested optimizations work. Due to the
               complexity fo the file-backed system, there could be subtle issues
               which we have not quite forseen. The estimate is between 1 to 2 months.

## Summarized work

| Work Item                             | Time                 | Priority  |
|---------------------------------------|----------------------|-----------|
| Write ConvertToMDVisualEventWorkspace | 6 to 11 months       | Very high |
| Distributed SaveMD                    | 2 to 6 months        | Very high |
| Performance BinMD                     | 1 to 2 months        | High      |
| ConvertToMDHisto                      | 2 to 4 months        | High      |
| Alternative Noramalization            | 1 to 2 days          | Medium    |
| Spherical Peaks in TOF                | 2 to 4 weeks         | Medium    |
