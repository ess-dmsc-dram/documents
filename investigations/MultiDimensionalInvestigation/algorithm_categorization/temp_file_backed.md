
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


### Parallel file-backed read and write



### Measurement of file-backed efficiency
