# Task List August 15-19

## Histogram 

- **High Priority**
	- Need to discuss what must be added to the Histogram type to make it more complete
	 - Starting point would be to look into search through [this list](https://github.com/mantidproject/mantid/issues/16118)
	 - `Kernel::VectorHelper` also contains some functionality we will want to add to histogram.

- **Lower Priority**
 - Planning the remainder of the Histogram Rollout. Algorithms is more than halfway complete but I may lose Dimitar very soon.
	- We can discuss timelines and when we hope to have the whole rollout complete.
 
## Indexing

- Go through design worked out so far
- Discuss a series of small or medium sized roadblocks
- Workspace creation is closely related to setting the `IndexTranslator`. This would be a good opportunity for creating a sensible `WorkspaceFactory`. Discuss details.
- 
## Instrument 2.0

Make progress with unimplemented [features](https://github.com/DMSC-Instrument-Data/documents/blob/master/meeting_notes/April_2016/InstrumentPrototype/README.md#step-scans)

**High Priority**
- Rotations, Required for write performance as well as scanning. How are we going to do rotations?
- Scanning Instrument, currently planned but not implemented
- Continuous Scans

**Lower Priority**
- Serialization (already underway)
- MPI (already underway little to be gained at this point. Dependent on serialization.)
