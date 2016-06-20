# Module Specification: HistogramData


## A) Scope

The scope of the module is generic.
It must not contain any instrument specific or facility specific data structures or operations.


## B) Scientific specification

### 1. Uncertainties

Operations provided by this module must handle statistical uncertainties of data.
In particular, uncertainties must always be propagated.

### 2. Data consistency

This module shall guarantee data consistency for high-level operations.
That is:

1. Sanity of input data shall be verified upon creation of data structures in the scope of this module.
2. Operations provided by this module shall not create invalid output data, given that their input data has been sanitized.
3. This module may provide low-level interfaces for direct access to underlying data in data structures. Low-level interfaces shall not sanitize input data.


## C) Technical specification

### 1. Dependencies

The dependencies of this module should be kept minimal.
In particular, there shall be no dependency on higher-level Mantid concepts such as geometry, instruments, workspaces, and algorithms.

### 2. Error handling

This module shall not log errors.
Logging would interfere with performance requirements in this low-level library.

Operations in this module shall raise an exception if an error occurs.

### 3. Thread-safety

Thread-safety of data structures in this module follows that of, e.g., `std::vector`.
That is:

1. Accessing an object simultaneously via `const` methods must be thread safe.
2. If one thread modifies an object, concurrent reading or writing shall not be possible.
3. Accesses to an object shall not interfere with accesses to other objects of the same type.

### 4. Documentation


## D) Examples

##### B.2

Consider the example of bin edges of a histogram.
The three items from B.2 imply, respectively:

1. When creating a bin-edges object, this module verifies that the bin width is strictly positive.
2. When modifying the bin-edge object by scaling it with a constant, this module verifies that the scale is, e.g., not zero to prevent bin width zero.
3. When directly accessing and modifying the `i`-th bin edge there is no validation, i.e., after this low-level access the bin width may negative or zero.
