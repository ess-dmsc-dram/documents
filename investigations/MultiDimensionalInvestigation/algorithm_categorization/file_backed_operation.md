# File-backed operation

Even at the current facilities data can become too large to hold all events in
memory (especially when several workspaces are merged), this has led to the
development of file-backed workspaces. The essence of these workspaces
is that events are only loaded into memory when they are required and removed
from memory when the are not longer needed. This can be done sine many
operations only require the box structure, which in this scheme is always
loaded into memory.

Below we want to discuss the basic mechanisms for file backed operation. As one
would hope, most of this is abstracted into the data structure itself and the
algorithms are not aware of it.


### Basic data structure enhancement

The basic data structure which holds actual data, i.e. the *MDBox*, contain an *MDBoxSavable*
instance which is an *ISaveable*. The *MDBoxSavable* contains a reference to its
box will ask the box to write itself to memory when required via the *save* method
or to release the events which are currently stored in memory via *clearDataFromMemory*.
This method will clear the *data* vector which contains the events in an *MDBox*.

Another thing to note is that events are given a boxId which is generated when
a *MDGridBox* is split into the a set of *MDBox* instances. The *BoxController*
provides a contiguous and incrementing index range for these boxes. This ID
is used to sort the boxes when they are saved to file later on. This ensures
that boxes which are children of the same grid and on the same level are
very close to each other on disk. This is used for optimization and in some
algorithms such as *SliceMD* and *BinMD* the binIDs are
explicitly sorted before they are saved to file.

An implementation detail which is quite relevant is the *DiskBuffer* class. It
stores boxes (or rather references to *MDBoxSavable* s) which we want to write
to disk. However it does not write each box individually to disk but waits until
a user-set write buffer size has been reached. The data gets written out
if it has never been written out, if the number of events has changed or if the
data has changed. If nothing has changed then the memory is freed by deleting
the *data* vector on the *MDBox* as mentioned above.


## Life cycle of boxes


#### 1. FileIDs
FileIDs are associated with each box and are used to store boxes to specific
positions in the file. The idea here is to have *MDBox* elements from
the same parent and at the same level to sit close to each other.  FileIDs are created when an *MDBox* splits into an *MDGridBox*. A new
start FileID is provided by the *MDBoxController*. In fact the box controller
will provide a contiguous block of FileIDs for the children. These are assigned
to the child boxes. **Note that this is potentially a bottle-neck for parallelization.**


#### 2. Save with file-backing enabled.

The main way to store a workspace to file in a file-backed mode is to
use the `MakeFileBacked` flat on *SaveMD*. Note that there is also the option
to just update a file-backed workspace using `UpdateFileBackEnd`.

An integral component for saving the workspace is *MDBoxFlatTree* which is
discussed [here](./load_and_save.md). The *MDBoxFlatTree* will store a pair
for each box which consists of a position on the file and the number of events in that box. The position on the file is obtained using the FileID of the box.
This information is also passed onto the box itself.

The *ISavable* member of each box is then queried. *MDGridBox* s are ignored.
With data is then saved at the required position.

Strangely it seems that the same result is obtained when not enabling `MakeFileBacked`
for the save algorithm. One thing to note is that the `ExperimentInfo` is stored out
separately as well.

#### 3. Loading the file-backed workspace

Basic information is extracted from the file and is used to create a simple
*MDEventWorkspace*.

TODO look at ExperimentInfo

The box structure is loaded into Mantid and rebuilt as described [here](./load_and_save.md). When we request a file-backed load operation, then
file position and the number of events are written into the *MDBox* which has been
restored. When requesting a file-backed load, the file information and a *BoxControllerNeXusIO* object are stored with the *BoxController*. We also set up
a maximum allowed cache.


#### 4. Operate on the file-backed workspac (BinMD)

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


#### Read and write for a distributed, visualization-optimized scenario

Read and write are handled separately here. If we only have to support
1. A dump of a distributed workspace to file
2. Reading from a file in order to populate a workspace without modifying
   the actual workspace
then we can most likely simplify the current operation since we don't require
a lot of the over head which is required to ensure that changes to a workspace
are synced with the file.

##### Read

###### Initial read-in

The initial read in *LoadMD* would be in principal
identical to the current usage since we load only
into a single machine. The box structure would be
loaded into memory. The data itself is not loaded
until it is being requested. It does not look like
we need to worry about much here.

###### Box updates

Updating the data vector of the boxes will occur when data is being rebinned. *BinMD* will require
precise knowledge of the distribution of events in the boxes to correctly calculate the bin signals. Currently *BinMD* does not operate in parallel for
file-backed workspaces. The way parallelization is introduced into this problem is to create space chunks and bin them separately. Two chunks might have to access the same *MDBox*, i.e. load the release data. This could lead to all sort off
odd behaviour. However, this should be avoidable by using a counter for the `busy` flag (treated atomically). In this way we should be able to allow for parallel
binning with file-backed workspaces. In fact we should be able to demonstrate this
with the current implementation.

##### Write

The *SaveMD* does not operate in a parallel manner. `HDF5` supports both
data writing with multiple threads and multiple processors. See [here](https://support.hdfgroup.org/HDF5/doc1.6/TechNotes/openmp-hdf5.c) and
 [here](https://support.hdfgroup.org/HDF5/Tutor/parallel.html). There is no
obvious locking in place (at least for the first-time save) which would make
data parallelism harder. Again this is something that would have to be tried out.

#### Measurement of file-backed efficiency

TODO:
  1. Create script which generates *MDEvent* data of varying size.
  1. Create script which loads MD workspace file-backed
  1. Performs various Bin operations
  1. Add measurement mechanism for the entire bin operation

See [here](./md_dummy_generator.py)
