### Neutron software

**Horace**: Alex explained the underlying data structure which is used in Horace to
  represent multi-dimensional data. It is essentially evenly gridded
  hypercube where each bin element points to a location of an event list.
  This event list can be stored on memory if the list does not fit into memory.
  The structure seems to be pretty much equivalent to an *MDEventWorkspace* where
  we set the level depth to 1 and ask for forced first-level-binning.

**MSlice**: This used to do it in the same way as Horace. In its current incarnation
            it makes use of Mantid features under the hood.

**Dave**: For visualization **Dave** uses *Mslice* according to [this](http://nvlpubs.nist.gov/nistpubs/jres/114/6/V114.N06.A04.pdf). Speaking to
Andrei, it appears that this would have taken from Horace.

**GSAS**: Does not seem to have too much information. The project seems to be
          dead.

### X-Ray Software

We want to have a look at x-ray software to check if groups in that area
have come up with good solutions for mult-dimensional data.

### Programs that were mentioned by Esko

**Dials**: This does not seem to have direct support for multi-dimensional
           data and/or visualization

**Mosflm**: It does not seem to support any multi-dimensional data.

**HKL3000**: Not clear if they have anything for multi-dimensional data,
            but it does not look like that. Multi-core processing is not supported.
