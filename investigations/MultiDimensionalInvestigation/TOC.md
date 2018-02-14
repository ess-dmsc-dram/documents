# Table of contents

For an overview of the thematic have a look at our [project presentation](./presentation/distributed_data_reduction_of_multi_dimensional_data.pptx).

## Documents

### User requirements

1. [Interaction log](./requirements_and_discussions/log.md)
1. [Summary of SCD and direct inelastic work-flows at the different facilites](./requirements_and_discussions/summary_of_workflows.md)
1. [Conclusion from requirements](./requirements_and_discussions/conclusion_from_requirements.md)

### Meeting notes
1. [Meeting notes 13/02/2018](./requirements_and_discussions/meeting_notes_2018_02_13.md)
2. [Meeting notes 14/02/2018](./requirements_and_discussions/meeting_notes_2018_02_14.md)


### Investigation of current multi-dimensional data structures
1. [*MDEventWorkspace*](./md_data_structures/md_event.md)
1. [*MDHistoWorkspace*](./md_data_structures/md_histogram.md)


### Categorization of the current multi-dimensional algorithms
1. [General categorization of algorithms](./algorithm_categorization/categorization.md)
1. [Description of current file-backed approach](./algorithm_categorization/file_backed_operation.md)
1. [Load and Saving of MD data](./algorithm_categorization/load_and_save.md)
1. [Investigation of purely event-based algorithms](./algorithm_categorization/pure_event_algorithm_description.md)
1. [Investigation of mixed-type algorithms](./algorithm_categorization/mixed_type_algorithm_description.md)

### Other distributed structures
1. [The Kitware approach](./distributed_data_structures/kitware.md)
1. [The naive approach](./distributed_data_structures/naive_approach.md)
1. Load balancing algorithms
   1. [Recursive Coordinate Bisection](./distributed_data_structures/recursive_coordinate_bisection.md)
   1. [Space Filling Curves](./distributed_data_structures/space_filling_curves.md)
   1. [Simon's split](./distributed_data_structures/simon_split.md)
1. [Other approaches](./distributed_data_structures/general.md)

### Other
1. [Investiation of event compression](./other/compress_event.md)
1. [ESS instrument resolutions: Estimating if a binned approach is feasible](./other/instruments_and_resolutions.md)
1. [Looking at other software packages](./other/other_software_packages.md)

### Prototypes
1. [Prototype for building distributed box strucutre](./prototype/Prototype.md)

### Visualization
1. [How can visualization be achieved?](./user_interaction/visualizations.md)

### Work items
1. [Implementation List](./to_implement/work_items.md)
1. [How to implement *ConvertToMDHistoWorkspace*](./to_implement/how_to_implement_convert_to_md_histo.md)
1. [How to implement *BinMD* for shared-memory-parallel file-backed operation](./to_implement/how_to_make_bin_md_parllel_for_file_backed.md)
1. [How to implement some TOF algorihtms such as IntegrateEllipsoids, etc](./to_implement/how_to_make_some_TOF_algs_MPI_compatible.md)


### Other documents
1. [Information for CSPEC](./requirements_and_discussions/pascale_info_1.pdf)
1. [Information for MAGiC 1](./requirements_and_discussions/xavier_info1.pdf)
1. [Information for MAGiC 2](./requirements_and_discussions/xavier_info2.pdf)
