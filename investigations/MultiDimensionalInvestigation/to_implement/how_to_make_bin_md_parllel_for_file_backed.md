# How to add parallel support to BinMD in the file-backed case

### Issue description

*BinMD* currently only supports parallel operation in a non-file-backed mode.
Parallelization is introduced via spatial chunks which are separately binned.
In the file-backed case this can lead to the following issue:

>Thread1 operates on binA in chunk1, while thread2 operates on binB in chunk2.
   *MDBox* C intersects both binA and binB. This means that the underlying events
   of the box need to be fetched from the file. This will lead two fetch requests
   which can overwrite data while it is being used and similarly delete data
   while it is being used (when the cache is clean up).`

### Potential solution
In the current scenario each thread is responsible for a set of bins but all
threads can access all boxes. One could think of a reversed scenario, where
each thread is responsible for a set of boxes, but all threads can access
all boxes. The advantage here is that only one thread will ever request that
events will be fetched from a box, hence allowing the disk buffer mechanism
to operate without "data races".

The implementation of the binning algorithm would look like:
1. Let the number of threads be T. Get all boxes (via depth-first search). We
partition the boxes on to the T threads. The box chunks will be close to each
other spatially, hence writing into the same box from several threads should be
rare and only occur and the boundaries of the responsibility of the threads.
2. Each thread iterates through its threads and evaluates which bins intersect
   with the box. There are three possibilities:
   * The box is not in the bin region, hence it cannot correspond to any bin
     of interest
   * The box is fully contained inside a bin. In this case the signal of the
     box is added to the bin value. There is no need to get the events from file.
   * The box intersects with one or several bins. In this case we need to
     efficiently compute which bins we are dealing with. Then we fetch the
     events from file and iterate over all events. We have signal variables for
     each of the possible bins and the event's signal is added to the correct signal variable.
     Once all events have been processed, we add the signal variables are atomically
     added to the bin signal.
