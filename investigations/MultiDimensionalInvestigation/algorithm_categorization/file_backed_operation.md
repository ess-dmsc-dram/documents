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
algorithms such as *SliceMD* and *BinMD* the binIDs are sorted before they are
explicitly sorted before saving them to file.

An implementation detail which is quite relevant is the *DiskBuffer* class. It
stores boxes (or rather references to *MDBoxSavable* s) which we want to write
to disk. However it does not write each box individually to disk but waits until
it a user-set write buffer size has been reached. The data gets written out
if it has never been written out, if the number of events has changed or if the
data has changed. If nothing has changed then the memory is freed by deleting
the *data* vector on the *MDBox* as mentioned above.
