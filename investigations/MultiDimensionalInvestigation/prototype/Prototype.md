# Prototype ConvertToDistributedMD

## Scope

This prototype takes a distributed event-type workspace, converts the events to MDEvents,
partitions the events between all ranks (in a load-balanced manner) and places the
events into a box strucure. As such each rank will contain a piece of a larger box structure.
The top-most part of the box structure's toplogy will be identical between all ranks,
but the different ranks will fill different parts of the box strucutre.

The resulting data structure (if it can be called that at all), is not meant to be
consumed by other algorithms, but this algorithms should save the data directly
to disk. Hence it should probably renamed SaveMDEventDistributed or similarly.



## Where to find prototype

The prototype is a branch in the Mantid repo, it can be found [here](https://github.com/mantidproject/mantid/tree/distributed_md_event_prototype).



## Explanation of the processing steps

We start with a distributed event workspace which we want to convert into a
data structure which resembles the `IMDNode` system of the `MDEventWorkspace`.
The steps to achieve this are

1. Convert the data which corresponds to the first n percent of the total measurement
2. Build a preliminary box structure on the master rank
3. Determine how the data will be split based on the preliminary box structure and share this information with all ranks
4. Share the preliminary box structure with all ranks
5. Convert all events
6. Add events to the local box structure
7. Send data from the each rank to the correct rank
8. Split the data
9. Ensure that the `fileID`s and the box controller stats are correct.
10. Save the data (not implemented yet)


We want to discuss each element individually

### 1. Get an n-percent fraction

The works is done by the `EventToMDEventConverter` class. `EventToMDEventConverter::getEvents` allows us to return only those events
which are within a certain time fraction of the full measurement, i.e. if we
specify to get the first `1%` then this means that we request the data which
was measured in the first `1%` of the pulse time. This does not necessarily mean
that we are requesting only the first 1% of the number of events that were measured, although that would be the same if the neutron flux was constant.

Note that this done on each rank.

### 2. Build a preliminary box structure on the master rank

This step has several sub steps which we need to execute:
1. We need to send sampled n-percent data from all ranks to the master rank. For
   this we use a combination of `boost::mpi::gather` to determine the array lengths
   which will be sent and `MPI_IRecv`-`MPI-ISendv` pairs.
2. The box structure is then built with the sample data from all the other ranks.
   Under the hood we build an `MDEventWorkspace` and extract the underlying box
     structure.


### 3. Determine the rank responisibility
Based on the preliminary box structure we determine which ranks will be
 responsible for which boxes using the `RankResponsibility` class. When performing
 a `IMDNode::getBoxes` call we get the box structure in a flat, vectorized form, which is being crated by traversing the box tree in a depth-first manner. This
 is similar to a space filling curve, i.e. boxes which are close to each other
 in momentum transfer space will be close to each other in the vector. Hence
 it makes sense to just assign contiguous segments of this vector to the different ranks. We make use of a box indices which is just the index of the vector.

 We get a `RankResponsibility` object which is just a vector of pairs where
 vector's index corresponds to the rank and the pair represents the start
 and end box index for which this rank is responsible. Note that the indices
 are inclusive.

We then share this responsibility with all ranks, i.e. each rank knows which
 box index range a particular rank is responsible for. This uses a `boost::mpi::broadcast` communication.

### 4. Share the box structure with all ranks
First we serialize the box structure using the `BoxStructureSerializer` class.
The serialized box structure is subsequently sent to all ranks. Note that this serialized box structure does not contain any events. This uses a `boost::mpi::broadcast` communication. The box structure is then deserialized on all ranks using the `BoxStructureSerializer` class. This box structure is stored together with the  `BoxController` in a `BoxStructureInformation` struct.


### 5. Convert all events
We convert all events on all ranks using the `EventToMDEventConverter` class.

### 6. Add events to preliminary box structure

We add the events on each rank to the empty box structure. The events will
trickle down the box structure until they hit a n `MDBox`. We don't ask the
`BoxController` to split the boxes if required. This means that on each
rank we still have the same box structure topology.

### 7. Send data from the each rank to the correct rank

Communication-wise this is the most complex step. Each rank A has a set of
boxes with continuous box indices X to Y which need to be sent to rank B, where
B is every other rank but A. We initially implemented this step by having a
communication on a per-box basis. This turned out to be very slow however and
it makes sense to group as much data into a single communication as possible.

### 8. Split the data
Split the data further on the local ranks.

### 9. Bring local box controllers into sync

The `fileID`s on the local ranks will not be in sync, e.g. we expect to
have duplicate `fileID`s on the different ranks. This is being consolidated
in this step.



## How to setup and use the Scarf cluster

This section just tries to generally capture how [Scarf](http://www.scarf.rl.ac.uk/) needs to be used.

### Access

Make sure that your register an account with [SCD](http://www.scarf.rl.ac.uk/contact-us). This will link your federal ID with
a Scarf account.

ssh in to Scarf via:
```
ssh YOUR_FED_ID@scarf.rl.ac.uk
```
and provide your password. In order to create a build you will want to create an
interactive session on the Rhel7 cluster
```
bsub -q scar-rhel7 -Is /bin/bash
```
You can verify that you run as a separate job now with
```
bjobs
```


### Setup

Make sure that you are in an interactive session as described above. Since most of our requirements to build Mantid are not met by Scarf and since
we don't have `sudo` rights, we need to run the five scripts in order:

1. `step_1_download_mantid.sh`
2. `step_2_install_dependencies.sh`
3. `step_3_run_cmake.sh`
4. `step_4_build_mantid.sh`
5. `step_5_set_env_var.sh`

in a folder
where we want our source, build and dependencies to be located. Note that this
will take a while to complete.

### Run an example

Let's say we have a dummy Python script `my_test.py` that we want to run :
```
import os
from mantid.simpleapi import LoadEventNexus, ConvertToDistributedMD
from mantid.kernel import mpisetup
import sys


# ------------------------------------------
# Load data
# ------------------------------------------
current_path = os.getcwd()
file_name = "mpi_test/TOPAZ_3132_event_10x.nxs"
full_file_name = os.path.join(current_path, file_name)

ws = LoadEventNexus(full_file_name)

# Make sure all ranks are in sync here
if 'boost.mpi' in sys.modules:
  mpisetup.boost.mpi.world.barrier()

# ------------------------------------------
# Run prototype
# ------------------------------------------
ConvertToDistributedMD(InputWorkspace=ws)
```
NB: Note that the `TOPAZ_3132_event.nxs` file would have to be in the root folder.

In order to run the above script we create a configuration script `run_my_script` which we
will want to launch:
```
#BSUB -q scarf-rhel7
#BSUB -n 310
#BSUB -x
#BSUB -m scarf17
#BUSB -W 01:00
#BSUB -o log.log
#BSUB -e err.err

LD_PRELOAD=/opt/ibm/platform_mpi/lib/linux_amd64/libmpi.so mpirun -lsf -np 300 -v  ~/ROOT_PATH/build/bin/mantidpython --classic ~/PATH_TO_SCRIPT/my_test.py
```

You can learn about the flags [here](https://www.ibm.com/support/knowledgecenter/en/SSETD4_9.1.2/lsf_command_ref/bsub.1.html).

Also note that we can run `mantidpython` only in classic mode since there are
issues when running IPython with a large number of nodes (concurrent access of the history data base causes a segfault).


In order to execute the script you just have to submit it as a job
```
bsub < run_my_script
```

You can monitor the output of the current job with `bpeek`, but note that you
cannot monitor on an interactive job. This means you will need a second
ssh session for monitoring.
