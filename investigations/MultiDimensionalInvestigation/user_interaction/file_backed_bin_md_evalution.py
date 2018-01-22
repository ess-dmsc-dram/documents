import random
import time
import matplotlib.pyplot as plt
import json
import numpy as np

# ------------------------------------------
# Create MDEventWorkspace
# -------------------------------------------
class MDEventCreator(object):
    x_min = -10
    x_max = 10
    y_min = -10
    y_max = 10
    z_min = -10
    z_max = 10
    def __init__(self, user_file_path=None):
        super(MDEventCreator, self).__init__()
        if user_file_path:    
            self.base_path_for_saving_file = os.path.join(user_file_path, "md_file_backed_test")
        else:
            self.base_path_for_saving_file = os.path.join(os.getcwd(), "md_file_backed_test")
 
    def generate_md_files(self, number_of_peaks_list, number_events_background=1e6, number_of_events_per_peak=1e7, use_cached=True):
        """
        Here we build up an MD workspace by specifying a certain number of events per peak and a certain number of peaks.
        """
        file_names = []
        for number_of_peaks in number_of_peaks_list:
            # Create file name
            file_name = "{}_{}.nxs".format(self.base_path_for_saving_file, number_of_peaks)
            file_names.append(file_name)

            # We want to check if an already file should be used. We sometimes don't want to reuse an existing file, since we might want to 
            # update the total number of events.
            if self.should_create_data(file_name, use_cached):
                # Get the md workspace
                ws = self.create_event_workspace( number_events_background=number_events_background,
                                                                                      number_events_per_peak=number_events_background,
                                                                                      number_of_peaks=number_of_peaks)

                # Save the md workspace
                self.save_workspace(ws,  file_name)
                 
        if mtd.doesExist("ws"):
            DeleteWorkspace("ws")
        return file_names
    
    def create_event_workspace(self, number_events_background, number_events_per_peak, number_of_peaks, split_into=5, split_threshold=1000, max_recursion_depth=5):
        start_time = time.time()
        # Extents
        extents_string = "{},{},{},{},{},{}".format(self.x_min,  self.x_max, self. y_min,  self.y_max, self.z_min, self.z_max)
        
        # Generate worksp
        ws = CreateMDWorkspace(Dimensions=3, 
                                                             EventType="MDEvent",
                                                             Extents=extents_string,
                                                             Names="x,y,z",
                                                             Units="x,y,z", 
                                                             SplitInto=split_into, 
                                                             SplitThreshold=split_threshold, 
                                                             MaxRecursionDepth=max_recursion_depth)

        # Add background
        self._add_background(ws, number_events_background)
        
        # Add peak
        self._create_peaks(ws, number_of_peaks, number_events_per_peak)
        
        # Report creation
        self._report_creation(ws, start_time, number_of_peaks)
        return ws

    def save_workspace(self, workspace, full_file_path):        
        start_time = time.time()
        SaveMD(InputWorkspace=workspace, FIlename=full_file_path, MakeFileBacked=True)
        end_time = time.time()
        message = ("\n++++++++++++++++++++++++++++++\n"
                               "Saving MD \n"
                               "Time taken: {} s"
                               "\n++++++++++++++++++++++++++++++\n".format(end_time-start_time))
        self._report(message)
        return full_file_path

    def should_create_data(self, file_name, use_cached):
        """ We want to create the data if it does not exist or when use_cached is set false    
               exists   |   use_cached  |    out  |
                  0                  0                       1
                  0                  1                       1
                  1                  0                       1
                  1                  1                       0
        """
        file_exists = os.path.exists(file_name)
        return not (file_exists and use_cached)

    def _report_creation(self, workspace, start_time, number_of_peaks):
        end_time = time.time()
        message = ("\n++++++++++++++++++++++++++++++\n"
                               "MD Event WorkspaceGeneration\n"
                               "Number Events: {}\n"
                               "Size: {}MB\n"
                               "Number of peaks: {}\n"
                               "Time taken: {} s"
                               "\n++++++++++++++++++++++++++++++\n".format(workspace.getNEvents(), 
                                                                                                                      workspace.getMemorySize()/1024/1024, 
                                                                                                                                     number_of_peaks,
                                                                                                                                     end_time-start_time))
        self._report(message)

    def _report(self, message):
        print(message)
        
    def _add_background(self, workspace, number_events_background):
        FakeMDEventData(InputWorkspace=workspace, UniformParams=number_events_background)

    def _create_peaks(self, workspace, number_of_peaks, number_of_events):
        for _ in range(number_of_peaks):
            x_position =  random.uniform(self.x_min, self.x_max)
            y_position =  random.uniform(self.y_min, self.y_max)
            z_position =  random.uniform(self.z_min, self.z_max)
            radius =  random.uniform(0.05, 0.3)
            peak_string = "{},{},{},{},{}".format(number_of_events, x_position, y_position, z_position,radius)
            FakeMDEventData(InputWorkspace=workspace, PeakParams=peak_string)

class MDLoadAndBinTest(object):
    def __init__(self):
        super(MDLoadAndBinTest, self).__init__()
        
    def run_test(self, number_of_peaks_list, use_cached=False, save_file_path=None):
        # Generate the files
        md_creator = MDEventCreator(save_file_path)
        file_names = md_creator.generate_md_files(number_of_peaks_list=number_of_peaks_list,
                                                                                                use_cached=use_cached)
         
        # Run the binning with a file backed workspace
        results_with_file_backed = self.run(file_names, file_backed=True)
        
        # Run the binning with a standard workspace
        results_without_file_backed = self.run(file_names, file_backed=False)
        
        return results_with_file_backed, results_without_file_backed
   
    def get_file_size(self, file_name):
       stats = os.stat(file_name)
       return stats.st_size
   
    def run(self, file_names, file_backed):
        workspace_sizes = []
        file_sizes = []
        number_events = []
        load_times = []
        number_of_slices = []
        average_bin_times = []
        std_bin_times = []
        number_of_md_boxes = []
        number_of_md_grid_boxes = []
        average_depth = []
        bin_times = []
        
        for file_name in file_names:
            # Load the file
            mtd.clear()
            ws, load_time = self.load_md(file_name, file_backed=file_backed)
            workspace_sizes.append(ws.getMemorySize()/1024./1024.)
            number_events.append(ws.getNEvents())
            load_times.append(load_time) 
            
            # Get box information
            bc = ws.getBoxController()
            number_of_md_boxes.append(bc.getTotalNumMDBoxes())
            number_of_md_grid_boxes.append(bc.getTotalNumMDGridBoxes())
            average_depth.append(bc.getAverageDepth())
            
            # Record file size
            file_sizes.append(self.get_file_size(file_name)/1024./1024.)

            # Perform binning measurement
            average_bin_time,  std_bin_time, num_of_slices, bin_time = self.bin(ws)
            average_bin_times.append(average_bin_time)
            std_bin_times.append(std_bin_time)
            number_of_slices.append(num_of_slices)
            bin_times.append(bin_time)
              
        # Add to results dict
        result = {}
        result["NumEvents"]=number_events
        result["WsSize"]=workspace_sizes
        result["FileSize"]=file_sizes
        result["LoadTime"]=load_times
        result["BinTime"]=average_bin_times
        result["BinTimeStd"]=std_bin_times
        result["NumSlices"]=number_of_slices
        result["NumBoxes"]=number_of_md_boxes
        result["NumGridBoxes"]=number_of_md_grid_boxes
        result["AvgDepth"]=average_depth
        result["BinTimes"]=bin_times
        return result
          
    def load_md(self, file_name, file_backed):
        start_time = time.time()
        if file_backed:
            ws = LoadMD(Filename=file_name, FileBackEnd=file_backed, Memory=300)
        else:
            ws = LoadMD(Filename=file_name, FileBackEnd=file_backed)
        total_time = time.time() - start_time
        
        message = ("\n++++++++++++++++++++++++++++++\n"
                       "LoadMD\n"
                       "Number Events: {}\n"
                       "Size: {}MB\n"
                       "Time taken: {} s"
                       "\n++++++++++++++++++++++++++++++\n".format(ws.getNEvents(), 
                                                                                                              ws.getMemorySize()/1024./1024., 
                                                                                                              total_time))
        self._report(message)
        return ws, total_time


    def bin(self, workspace):
        """ 
        This is the actual test. We want to take several slices. The idea is to take a moving x-y slab.
        """
        thickness = 0.1
        z_position = np.linspace(-7,7,num=50)
        qz_values  = ["z,{},{}, 1".format(min_value, min_value+thickness) for min_value in z_position]
        
        bin_times = []
        
        for qz_value in qz_values: 
             start_time = time.time()
             binned = BinMD(InputWorkspace=workspace, 
                                     AlignedDim0='x,-1.5,1.5,200',
                                     AlignedDim1='y,-1.5,1.5,200', 
                                     AlignedDim2=qz_value)
             end_time = time.time()
             bin_times.append(end_time-start_time)
        
        # Get the time statistics
        average_time = np.mean(bin_times)
        std_time = np.std(bin_times)
        
        message = ("\n++++++++++++++++++++++++++++++\n"
                       "Binning \n"
                       "Slices taken: {}\n"
                       "Size: {}MB\n"
                       "Number Events: {}\n"
                       "Agerage time taken: {} s"
                       "\n++++++++++++++++++++++++++++++\n".format(len(qz_values), workspace.getMemorySize()/1024./1024., workspace.getNEvents(), average_time))
        self._report(message)
        return average_time, std_time, len(qz_values) , bin_times       
        
    def _report(self, message):
        print(message)
                  
class JsonDump(object):
    @staticmethod    
    def write(data, file_name):
        if os.path.exists(file_name):
            os.remove(file_name)
        with open(file_name, 'w') as f:
            json.dump(data, f)

    @staticmethod    
    def read(file_name):
        if not os.path.exists(file_name):
            raise RunTimeError("The file {} does not exist".format(file_name))
        with open(file_name, 'r') as f:
            data = json.load(f)
        return data

class ResultAnalysis(object):
    def __init__(self):
        super(ResultAnalysis, self).__init__()
        
    def get_plot_data(self, data_set):
         bin_times = data_set["BinTimes"]
         file_sizes = data_set["FileSize"]
         
         file_sizes = [[element]*len(bin_times[0]) for element in file_sizes ]
         
         bin_times = [e for l in bin_times for e in l]
         file_sizes = [e for l in file_sizes for e in l]
         return file_sizes, bin_times
        
    def evaluate_load_and_bin(self, results_with_backend_file_name, resuls_without_backend_file_name):
        results_with_backend = JsonDump.read(results_with_backend_file_name)
        results_without_backend = JsonDump.read(resuls_without_backend_file_name)
        
        file_sizes_with_backend, bin_times_with_backend = self.get_plot_data(results_with_backend)
        file_sizes_without_backend, bin_times_without_backend = self.get_plot_data(results_without_backend)

        plt.close('all')
        
        # ----------------------------------------------
        # Generate file size plots
        # ----------------------------------------------
        fig, axes = plt.subplots(4, 2, sharex=True)
        fig.suptitle("File Size effects", fontsize=18)
        
        # BIN TIME vs FILE SIZE
        axes[0,0].errorbar(results_with_backend["FileSize"],  results_with_backend["BinTime"], yerr=results_with_backend["BinTimeStd"] ,fmt="ro", label="File-backed")
        axes[0,0].errorbar(results_without_backend["FileSize"],  results_without_backend["BinTime"], yerr=results_without_backend["BinTimeStd"], fmt="bo", label="Not file-backed")
        axes[0,0].set_ylabel("Bin Time [s]")
        
        # WORKSPACE SIZE vs FILE SIZE
        l1, = axes[1,0].plot(results_with_backend["FileSize"],  results_with_backend["WsSize"], "ro", label="File-backed")
        l2, = axes[1,0].plot(results_without_backend["FileSize"],  results_without_backend["WsSize"], "bo", label="Not file-backed")
        axes[0, 0].legend(handles=[l1, l2], loc=2) 
        axes[1,0].set_ylabel("Workspace Size [MB]")
       
        # WORKSPACE SIZE vs FILE SIZE
        axes[2,0].plot(results_with_backend["FileSize"],  results_with_backend["LoadTime"], "ro", label="File-backed")
        axes[2,0].plot(results_without_backend["FileSize"],  results_without_backend["LoadTime"], "bo", label="Not file-backed")
        axes[2,0].set_xlabel("File Size [MB]")
        axes[2,0].set_ylabel("Load Time [s]")  
               
        # RAW vs FILE SIZE
        axes[3,0].plot(file_sizes_with_backend,   bin_times_with_backend, "ro", label="File-backed")
        axes[3,0].set_xlabel("File Size [MB]")
        axes[3,0].set_ylabel("Raw Bin Time File-backed [s]")
        
        # RAW vs FILE SIZE
        axes[3,1].plot(file_sizes_without_backend,   bin_times_without_backend, "bo", label="Not file-backed")
        axes[3,1].set_xlabel("File Size [MB]")
        axes[3,1].set_ylabel("Raw Bin Time non File-backed [s]")
        
        
        # NUMBER OF BOXES vs FILE SIZE
        results_with_backend["NumBoxes"] = [element/1e6 for element in results_with_backend["NumBoxes"]]
        results_without_backend["NumBoxes"] = [element/1e6 for element in results_without_backend["NumBoxes"]]
        axes[0,1].plot(results_with_backend["FileSize"],  results_with_backend["NumBoxes"], "ro", label="File-backed")
        axes[0,1].plot(results_without_backend["FileSize"],  results_without_backend["NumBoxes"], "bo", label="Not file-backed")
        axes[0,1].set_xlabel("File Size [MB]")
        axes[0,1].set_ylabel("Number of Boxes [x1e6]")
       
        # NUMBER OF GRID BOXES vs FILE SIZE
        results_with_backend["NumGridBoxes"] = [element/1e6 for element in results_with_backend["NumGridBoxes"]]
        results_without_backend["NumGridBoxes"] = [element/1e6 for element in results_without_backend["NumGridBoxes"]]
        axes[1,1].plot(results_with_backend["FileSize"],  results_with_backend["NumGridBoxes"], "ro", label="File-backed")
        axes[1,1].plot(results_without_backend["FileSize"],  results_without_backend["NumGridBoxes"], "bo", label="Not file-backed")
        axes[1,1].set_xlabel("File Size [MB]")
        axes[1,1].set_ylabel("Number of GridBoxes[x1e6]")
        
        # NUMBER OF Events vs FILE SIZE
        results_with_backend["NumEvents"] = [element/1e6 for element in results_with_backend["NumEvents"]]
        results_without_backend["NumEvents"] = [element/1e6 for element in results_without_backend["NumEvents"]]
        axes[2,1].plot(results_with_backend["FileSize"],  results_with_backend["NumEvents"], "ro", label="File-backed")
        axes[2,1].plot(results_without_backend["FileSize"],  results_without_backend["NumEvents"], "bo", label="Not file-backed")
        axes[2,1].set_xlabel("File Size [MB]")
        axes[2,1].set_ylabel("Number of Events[x1e6]")
       
        plt.show()

# -------------------------
# Execute test
# -------------------------
# The save file path can be used to test the influence of a particular hard drive type.
save_file_path = None
load_and_bin_test = MDLoadAndBinTest()
num_peaks_list = [30, 50, 90, 140, 150]  
num_peaks_list = [5, 10, 20, 40,  80, 130]  
res_fb, res_no_fb = load_and_bin_test.run_test(num_peaks_list, use_cached=True, save_file_path=save_file_path)

# Store the results asj json
file_path_with_file_backed = os.path.join(os.getcwd(), "results_with_file_backed.json")
file_path_without_file_backed = os.path.join(os.getcwd(), "results_without_file_backed.json")
#JsonDump.write(res_fb, file_path_with_file_backed)
#JsonDump.write(res_no_fb, file_path_without_file_backed)

# Evaluate
analysis = ResultAnalysis()
analysis.evaluate_load_and_bin(file_path_with_file_backed, file_path_without_file_backed)

