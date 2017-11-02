# Kitware's distribted data sets

Steve has pointed us to:
* [Composite Datasets](https://www.paraview.org/Wiki/VTK/Tutorials/Composite_Datasets)
* [vtkCompositeDataSet](https://www.vtk.org/doc/nightly/html/classvtkCompositeDataSet.html)
* [vtkMultiBlockDataSet](https://www.vtk.org/doc/nightly/html/classvtkMultiBlockDataSet.html)

for potential distributed (and sparse, hierarchical) data sets. However looking into these elements, they don't seem to
have a direct connection with distributed data sets, but they can be rather used to build sparse, hierarchical data sets.


## vtkDataObject family
The composite data set can be comprised of
* vtkHierarchicalBoxDataSet
* vtkMutliBlockDataSet
* vtkMultiPieceDataSet

![VTK](vtk_data_set_family.png)

### vtkMultiBlockDataSet
vtkMultiBlockDataSet is a dataset comprised of blocks. Each block can be a non-composite vtkDataObject subclass (or a leaf) or an instance of vtkMultiBlockDataSet itself.
**This makes is possible to build full trees**. vtkHierarchicalBoxDataSet is used for AMR datasets which comprises of refinement levels and uniform grid datasets at each refinement level.

### vtkMultiPieceDataSet

Here the elements cannot be a block themselves.


# From Reading

### vtkDistributedDataFilter

From the documentation:
> This filter redistributes data among processors in a parallel application into spatially contiguous vtkUnstructuredGrids. The execution model anticipated is that all processes read in part of a large vtkDataSet. Each process sets the input of filter to be that DataSet. When executed, this filter builds in parallel a k-d tree, decomposing the space occupied by the distributed DataSet into spatial regions. It assigns each spatial region to a processor. The data is then redistributed and the output is a single vtkUnstructuredGrid containing the cells in the process' assigned regions.

TODO: Continue when appropriate
