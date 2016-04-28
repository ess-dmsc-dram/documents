# SpectrumNumber/Index discussion

Discussion based on [design document](https://github.com/mantidproject/documents/blob/spectrum_number_and_workspace_index_abstraction/Design/spectrum_number_and_workspace_index_abstraction.md).

Next steps:
- Understand `MatrixWorkspace`:
  - What parts of the interface are related to spectrum number / index translation?
  - Which parts need to be kept and which need to be replaced?
  - Where should the code be moved? Is `MatrixWorkspace` the right place?
- `class IndexSet` may need refinement.
  - Need a workspace for validation. Who does the validation? Create a new type that defines the mapping, instance of type could live in workspace (replacing the current maps there), and could be used for validation?
- Figure out if `SpectrumAlgorithm` is the right way of doing this, in particular:
  - The generic definition of properties related to index ranges and list.
  - Is this the right place for the validation code?
- Figure out how the algorithm interfaces can support both spectrum-number and workspace-index.

Detector ID:
- Similar to spectrum-number case, but detector ID definition is fixed for an instrument, i.e., is the same for all workspaces of a given instrument.
- Any roll-out effort that changes things on the client side (in particular Algorithms) will make instrument-2.0 easier.
- Effort for changes inside the actual instrument (1.0) code should be considered carefully, they may not be worth doing.
