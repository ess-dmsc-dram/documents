# How to implement ConvertToMDHisto

## Single rank solution
This document explains the rough steps that are required to calcualte an
*MDHistoWorkspace* on a single rank from a distributed *EventWorkspace*.

1. Convert the local spectra into a local *MDHistoWorksapce* (This needs to be
  discussed in detail how to achieve this, but it is a local operation.)
2. We have the data on p ranks. We perform pairwise merging of the *MDHistoWorkspace* s.
   This works in the following manner.
   1. Send the data of each odd rank to its neighbouring, lower-valued rank, i.e.
      Data is sent from rank 1 to rank 0, rank 3 to rank 2, etc.
   2. Combine the data.
   3. Now we have data on rank 0, 2, 4, .... and possibly rank p-1 if we started
      off with an uneven number of elements.
   4. Perform a similar operation as in step 1. until all the data has been
      combined on one rank.

  The only issue that needs to be solved is how to serialize the data from an
  *MDHistoWorkspace* in order to transmit it to the receiving rank. As mentioned
  [here](../md_data_structures/md_histogram.md) the underlying data in an *MDHistoWorkspace*
  is stored as single vector. This information can easily be transmitted via
  MPI.

The above shows that solving the direct conversion from *EventWorkspace* data
to *MDHistoWorkspace* in a non-distributed way already solves the problem. This
would work in the following way:
1. Create an empty *MDHistoWorksapce* with the desired binning.
2. Convert each event as implemented in *ConvertToMD* and place it into its
   correct bin.
