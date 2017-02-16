# Index property and related bits

Notes for call between Lamar and Simon, 2017-02.16.

## Relevant links

- [High level overview](https://github.com/mantidproject/documents/blob/master/Presentations/Review_Meetings/plans_indexing_changes.md)
- [Design document](https://github.com/mantidproject/documents/blob/master/Design/spectrum_number_and_workspace_index_abstraction.md)
- [Rollout notes](https://github.com/mantidproject/documents/blob/master/Design/indexing_rollout_notes.md)

Most of these documents are slightly outdated, e.g., naming of some classes.

## IndexInfo and MPI

- The effort for the full rollout is probably much more than 1 year. Cannot afford to do this.
  - `ISpectrum` notifies `IndexInfo` about changes. We can thus have `IndexInfo` even without rollout
  - For MPI support this mechanism is not really feasible. Thus, we will probably support MPI only in algorithms that do not use the legacy interface (`ISpectrum::setSpectrumNo()`, etc.), will "port" algorithms to MPI support as needed.
- It is not feasible to maintain a mapping from detector ID to spectra with the legacy interfacce. This is too costly and too cumbersome.
  - Build mapping on demand (replacing the corresponding methods for build mappings in `MatrixWorkspace`).
  - Make it nicer than now (client code creates translation class, can specify desired behavior, such as accepting or refusing non-unique mappings fro detectors, etc.).
  - Support MPI internally.
  
See [this branch]() for some updates for `IndexInfo` (work in progress, don't base work on this currently).
  
## Index property
  
  - See high level overview.
  - Maybe having this as part of a workspace property would be best, then we can validate directly and algorithms to not need to take 3 steps to get indices, so instead of doing:
    
    ```python
    ws = getProperty(InputWorkspace)
    indexInfo = ws.indexInfo()
    spectrumRange = getProperty(SpectrumRange)
    indices = indexInfo.makeSpectrumIndexSet(spectrumRange)
    ```
    
    We could do simpler with a unified property:
    
    ```python
    ws, indices = getProperty(InputWorkspace)
    ```
