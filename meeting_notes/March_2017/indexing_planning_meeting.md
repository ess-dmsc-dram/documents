# Indexing Info Planning Meeting

## March 13-15 2017

## Attendees

- Simon Heybrock (SH)	 
- Lamar Moore (LM)

## Core Indexing and MPI Work

### IndexInfo
SH extended the functionality of the `IndexInfo` class to include translation and partitioning (MPI rank distribution). There
have also been strongly typed replacements for `detid_t` and `specnum_t`. One of the major concerns with the new `IndexInfo` class was the interplay with the legacy `ISpectrum` interface. In particular, maintaining a valid list of spectrum numbers across ranks with multiple mechanisms for modifying spectra. `IndexInfo` has a policy which only allows the spectrum numbers to be updated using a global spectrum list `IndexInfo::setSpectrumNumbers(std::vector<SpectrumNumber> &&spectrumNumbers)`. Each rank will build a list by extracting only relevant spectra. On the other hand, `ISpectrum` allows modification of individual spectra within the rank. This could lead to a condition where the global spectrum list becomes invalid. If the state of the global list is invalidated for ever call to `ISpectrum::setSpectrumNumber(specnum_t spectrumNumber)`, expensive interprocess communication would be required to create a valid list of spectrum numbers within the lazy update mechanism of `IndexInfo`:

```cpp
std::vector<Indexing::SpectrumNumber> myLocalSpectrumNumbers;
// MPI...
std::vector<std::vector<Indexing::SpectrumNumber>> allLocalSpectrumNumbers;
// merge
// (partition index, local spectrum index) -> global spectrum index
std::vector<size_t> current(numberOfPartitions, 0);
for(size_t i=0; i<globalNumberOfHistograms(); ++i) {
  auto partition = partitioner.indexOf(i);
  allSpectrumNumbers.push_back(
      allLocalSpectrumNumbers[partition][current[partition]]);
  current[partition]++;
}
std::vector<Indexing::SpectrumNumber> allSpectrumNumbers; // indexed by GlobalSpectrumIndex
m_indexInfo->setSpectrumNumbers(std::move(allSpectrumNumbers));
```

For a (to be added) MPI build of Mantid, the decision was made to forbid legacy functionality for modifying the spectrum numbers in `ISpectrum` which obviates the need for interprocess communication.

SH has assigned the update PR to LM for review. This will provide the opportunity for LM to solidify understanding of the partitioning and translation mechanisms and suggest any improvements which may be required to the interface. 

### MatrixWorkspace maps

`MatrixWorkspace` provides several methods which map between DetectorID and Spectrum Index/Spectrum Number. Instead of maintaining these maps in IndexInfo, SH believed it would be better to create these maps at the point where they are required. A very basic two part interface was designed which would satisfy the majority of use cases:

```cpp
class DetectorIDToSpectrumIndex {
public:
  bool isOnThisRank(DetectorID id) {
    // Simple case: Assuming 1:1 mapping between spectra and detectors, i.e.,
    // there is a spectrum for each detector.
    if(!detectorInfo.detectorIDs().contains(id))
      throw;

    // Alternative: More complex case: Not all detectors have a
    // corresponding spectrum
    //if(!m_allDetIDs.contains(id))
    //  throw;

    return m_detIDToIndex.contains(id);
  }

  size_t indexOf(DetectorID id) {
    return m_detIDToIndex.at(id);
  }

private:
  std::map<DetectorID, size_t> m_detIDToIndex;
  //std::vector<DetectorID> m_allDetIDs; // detector ids from all ranks that are part of a spectrum
};
```
LM to come up with final design and ensure this will be compatible with MPI. Initially, algorithms (mostly file loaders) which use these mechanisms will be ignored until a later time. This mapping will complement the work on the Index Property (mentioned below).

### Distributed file loading

LM to investigate what would be required to allow parallel file loading using MPI. `LoadEventNexus` will be the case study for this investigation. LM will do initial profiling to determine if there is any discrepancy between maximum disk read spead and algorithm execution time. The initial thoughts on this are to use a single rank to load data and distribute on other ranks. The outcome of this work could also be extended to data streaming where adding events to `EventLists` could produce a major bottle neck. This is based on early tests performed by SH on the live streaming mechanism in Mantid. LM to discuss with Matt Jones.
 
## WorkspacePropertyWithIndex

The index property was suggested as a mechanism for cleaning up the current mess with indexing in mantid algorithms. Graphically this property could take the form:

```
(*) Spectrum Number | ( ) Detector ID | ( ) Workspace Index
List: [                   ] e.g 1-100 or 1, 5, 6, 200 etc.
``` 

Users could then declare the property using flags to determine which index types are allowed:
```cpp
declareProperty(make_unique<IndexProperty>("InputIndices", UseSpectrumNumber|UseDetectorID|UseWorkspaceIndex));
```

The `IndexInfo` translation methods could then be used to retrieve the correct indices for a specific rank:
```cpp
const MatrixWorkspace_const_sptr inputWS = getProperty("InputWorkspace");

const auto indexSet = inputWS.indexInfo().makeIndexSet(getProperty("InputIndices"));
```

Although this mechanism would provide a workable solution, it results in rather ugly code and requires the developer to know that the index property cannot be used directly. An alternative would be to combine this property with the workspace property.
This would not only allow a more compact definition and retrieval mechanism, but would also allow validation to occur before the algorithm is executed to force the correct user input. Properties would then be declared using:

```cpp
declareProperty(make_unique<WorkspacePropertyWithIndex>("InputWorkspaceAndIndex", UseSpectrumNumber|UseDetectorID|UseWorkspaceIndex));
```

Users would then retrieve a tuple of values:
```cpp
//c++ 11
const MatrixWorkspace_const_sptr inputWS;
const IndexSet indexSet;
std::tie(inputWS, indexSet) = getProperty("InputWorkspaceAndIndex");

//c++ 17
auto [inputWS, indexSet} = getProperty("InputWorkspaceAndIndex");
```

or in python:
```python
inputWS, indexSet = getProperty("InputWorkspaceAndIndex");
```

LM is to come up with design options and provide estimates on producing this workspace property. The current idea is to use a composite of `WorkspaceProperty` and `ArrayProperty`. Implementation of this property will be placed on hold until final decisions regarding Mantid 4.0 and the indexing work have been made. SH, Owen Arnold, Jon Taylor and Nick Draper to provide final answers.

## High Level Road-map for Indexing

- LM and Owen Arnold to review IndexInfo PR and get this into master
- SH continue to augment IndexInfo with more MPI functionality
- SH will return to the MPI proof of concept and get to a stage where we have an MPI build of Mantid.
- LM and SH will refactor selected algorithms (mixture of trivial and non-trivial cases).
- Initial limited working MPI build of Mantid with some algorithms able to perform parallel reduction.  

## Kafka Streaming

LM had a brief discussion with Jon Taylor and SH about the work done so far on Kafka Streaming. Jon mentioned that filtering events should be done on a frame-by-frame basis before anything else happens with the event data. SH made suggestions about introducing a microservice which filters bad events and either re-streams the filtered event data (exits as a separate process), or conveys the filtered data directly to the accumulated workspace (exists as part of the listener). SH also expressed concerns that current data rates may be seriously reduced when dealing with event lists. The current Kafka stream uses a single event list for all events which may be producing unrealistic data rates. LM to discuss further with Matt Jones.

## Instrument View

SH indicated that the performance of the instrument view may become a critical factor during the instrument commissioning phase at the ESS. LM to profile current performance for complex instrument geometries (> 10^6 pixels, Voxels, Rectangular Detectors, Tubes). After instrument workshops at ESS, the team needs to determine bottom line functionality required for the instrument view. SH and Jon Taylor believe users should not have to use paraview, there should be a simple implementation of thresholding which allows inspection of instrument layers. SH to discuss scanning in the instrument view with Owen and Roman.


