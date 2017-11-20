
TODO: merge with file_backed_operation.md


### File-backed operation in BinMD

*BinMD* is an instructive example to understand how events are fetch and
release from the file. It is also the only algorithm that is needed for
visualization in the *SliceViewer*.

Remember that the entire box structure is stored in memory and that when a
leaf node is reached the algorithm can query the events, for example, via
`getEvents`. This will return an `std::vector` of the appropriate event
type. In the standard case this is stored in memory. However in the case
of file-backed execution this is not necessarily the case. Several things happen

1. The box is loaded via `MDBox::loadAndAddFrom`. The box knows how
   many events it has stored and what the file position is. `BoxControllerNeXusIO::loadBlock` will retrieve the data from the
   NeXus file and the data is added to the `data` vector of the box.
   Note that the loading is handled by the member of type `MDBoxSavable`.
2. The `MDBoxSavable` is set to `busy`. This essentially tells the "clean-up"
   logic to not clean the data vector for this box.
3. The `MDBoxSavable` is added to the `DiskBuffer` (which is a member of the box
   controller). It is added to an queue and processed. There are several
   scnearios which deal with changes in the number of events for example. It
   will save them out. There are two details which are of interest at this
   point.
   1. The processing of `MDBoxSavable` only occurs if there are sufficiently
      many `MDBoxSavable`s in the buffer (above a user-set threshold).
   2. Data which is set to busy is not processed and re-queued. Queue-processing
      is not scheduled via a timer but triggered with every `getEvents` call.
      They way the `MDBoxSavable` is processed depends on various things, e.g.
      if the number of data elements has changed, if the data itself has changed
      or if nothing has changed. In any case the last operation will always be
      an (indirect) call to `MDBox::clearDataFromMemory` which sets `MDBox::data`
      to an empty vector.
   3. Elements which are busy are re-queued as mentioned above.    
4. The *BinMD* uses the event data to calculate which event contributes to which
   bin. Other algorithms might alter the event list or generate new boxes. This
   will be eventually handled by the `DiskBuffer` to ensure that the changes
   are synced with the file and that events are removed from memory.
5. After *BinMD* is done, the `MDBoxSavable` is set to `not-busy`. This will
   ensure that the box (which at this point is still in the queue of the
   `DiskBuffer` is handled correctly and the data in memory is cleared.


### Read and write for a distributed, visualization-optimized scenario

Read and write are handled separately here. If we only have to support
1. A dump of a distributed workspace to file
2. Reading from a file in order to populate a workspace without modifying
   the actual workspace
then we can most likely simplify the current operation since we don't require
a lot of the over head which is required to ensure that changes to a workspace
are synced with the file.

#### Read

##### Initial read-in

The initial read in *LoadMD* would be in principal
identical to the current usage since we load only
into a single machine. The box structure would be
loaded into memory. The data itself is not loaded
until it is being requested. It does not look like
we need to worry about much here.

##### Box updates

Updating the data vector of the boxes will occur when data is being rebinned. *BinMD* will require
precise knowledge of the distribution of events in the boxes to correctly calculate the bin signals. Currently *BinMD* does not operate in parallel for
file-backed workspaces. The way parallelization is introduced into this problem is to create space chunks and bin them separately. Two chunks might have to access the same *MDBox*, i.e. load the release data. This could lead to all sort off
odd behaviour. However, this should be avoidable by using a counter for the `busy` flag (treated atomically). In this way we should be able to allow for parallel
binning with file-backed workspaces. In fact we should be able to demonstrate this
with the current implementation.

#### Write

The *SaveMD* does not operate in a parallel manner. `HDF5` supports both
data writing with multiple threads and multiple processors. See [here](https://support.hdfgroup.org/HDF5/doc1.6/TechNotes/openmp-hdf5.c) and
 [here](https://support.hdfgroup.org/HDF5/Tutor/parallel.html). There is no
obvious locking in place (at least for the first-time save) which would make
data parallelism harder. Again this is something that would have to be tried out.

### Measurement of file-backed efficiency

TODO:
  1. Create script which generates *MDEvent* data of varying size.
  1. Create script which loads MD workspace file-backed
  1. Performs various Bin operations
  1. Add measurement mechanism for the entire bin operation

See [here](./md_dummy_generator.py)
