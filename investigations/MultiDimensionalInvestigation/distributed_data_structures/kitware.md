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
