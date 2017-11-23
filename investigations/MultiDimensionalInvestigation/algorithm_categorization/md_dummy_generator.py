import os
import time
from mantid.kernel import config
import mantid.simpleapi as sapi


def create_md_dummy_workspace(multiples=1, number_of_events=1000, split_threshold=10000):
    # -------------------------------------
    # Create EventWorkspace
    # ------------------------------------
    start_time = time.time()
    ws = sapi.CreateSampleWorkspace(WorkspaceType="Event", NumEvents=number_of_events,Random=True,Function="Multiple Peaks")
    for _ in range(multiples):
        buffer = sapi.CreateSampleWorkspace(WorkspaceType="Event", NumEvents=number_of_events,Random=True,Function="Multiple Peaks")
        ws= sapi.Plus(ws, buffer)
    if mtd.doesExist("buffer"):
        sapi.DeleteWorkspace(buffer)

    sapi.SetUB(Workspace=ws,a='1.4165',b='1.4165',c='1.4165',u='1,0,0',v='0,1,0')
    print("Generation of EventWorkspace took: {}s".format(time.time() - start_time))
 
    # -------------------------------------
    # ConvertToMD
    # ------------------------------------
    start_time = time.time()
    md_ws=sapi.ConvertToMD(InputWorkspace=ws, deAnalysisMode="Elastic", Q3DFrames="Q_lab", QDimensions="Q3D",
                                                                                                                            MinValues='-20,-20,-20',MaxValues='20,20,20',SplitInto='50,50,50',
                                                                                                                            SplitThreshold=split_threshold)
    print("Conversion to MD took: {}s".format(time.time() - start_time))

    # -------------------------------------
    # Clean up
    # ------------------------------------ 
    DeleteWorkspace(ws)
    return md_ws


def provide_file_backed(multiples=1, number_of_events=1000, file_backed=True):
        test_workspace_name = "md_file_backed_test_multiples{}.nxs".format(multiples)

        file_path = os.getcwd()
        full_file_path = os.path.join(file_path, test_workspace_name)
        print("The file path is {}.".format(full_file_path))
        if not os.path.exists(full_file_path):
            print("Saving file")
            buffer_ws = create_md_dummy_workspace(multiples=multiples,number_of_events=number_of_events)
            start_time = time.time()
            sapi.SaveMD(InputWorkspace=buffer_ws, FIlename=full_file_path, MakeFileBacked=file_backed)
            sapi.DeleteWorkspace(buffer_ws)
            print("Saving the file took: {}s".format(time.time() - start_time))
       
        start_time = time.time()
        file_backed_workspace = sapi.LoadMD(Filename=full_file_path, FileBackEnd=file_backed, Memory=300)
        
        print("The size of the loaded MD file is {}MB.".format(file_backed_workspace.getMemorySize()/1000/1000))
        print("Loading the data took: {}".format(time.time() - start_time))
        return file_backed_workspace


def test_bin_md(original_workspace, repetitions):
    start_time = time.time()
    for _ in range(repetitions):
        binned = sapi.BinMD(InputWorkspace=original_workspace,  
                                   AlignedDim0='Q_lab_x,-5,5,500',
                                   AlignedDim1='Q_lab_y,-5,5,500', 
                                   AlignedDim2='Q_lab_z,-1,1,1')
    print("The average bin time was {}s".format((time.time()-start_time)/repetitions))



# ------------------------------------------
# Settings
# ------------------------------------------
data_multiples = 1
bin_reps = 3
num_events=1000

mtd.clear()
print("+++++++++++++++")
out = provide_file_backed(multiples=data_multiples, number_of_events=num_events)
test_bin_md(original_workspace=out, repetitions=bin_reps)

mtd.clear()
print("+++++++++++++++")
out2 = provide_file_backed(multiples=data_multiples, number_of_events=num_events,  file_backed=False)
test_bin_md(original_workspace=out2, repetitions=bin_reps)



