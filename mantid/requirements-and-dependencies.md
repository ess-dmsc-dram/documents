# Requirements and Dependencies for Data Reduction with Mantid at ESS

## Instrument

#### ESS

- beamlines with up to 10 million detectors
- 3D detectors with complex pixel shapes
- non-straight beam paths in all instruments
- scanning in a few instruments

#### Mantid

- horrendous performance
- no well-defined interface (all algorithms are forced to do low level interaction)
- limited feature set
- complexity makes it hard to modify
- lack of well-defined interface implies that many functionality changes require changes in hundreds of algorithms

#### Strategy

- design replacement for the `Instrument` part of the Mantid `Geometry` module (`Beamline` module)
- high-level interface, initially introduced as a wrapping layer, caters for the instrument access needs of 90% of all algorithms, will later allow for an easy replacement of the underlying logic


## Indexing

#### ESS

#### Mantid

- spectrum numbers and detector IDs used every internally
- no unified validation and translation between index types
- using IDs instead of plain indices implies extra cost for translation via maps



## MPI

#### ESS

- target data rates can not be handled on a single node
- memory requirements too high

#### Mantid

- MPI for some special cases at SNS

#### Strategy

- MPI for `MatrixWorkspace` (basically a list of spectra) very simple in many cases
- cannot work without having proper index handling
- index handling should be fixed properly, but this requires a very high effort
- investigate workaround that might allow us to do so only for algorithm that we want to have MPI support
