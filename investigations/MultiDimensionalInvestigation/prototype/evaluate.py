import os
from collections import namedtuple

import matplotlib.pyplot as plt
import numpy as np


file_information = namedtuple("file_information", 'number_of_ranks, file_name')
measurement = namedtuple("measurement", "number_of_ranks, mean, std, raw")


class Evaluate:
    def __init__(self, path_to_data):
        self.path_to_data = path_to_data

        self.cpu_time_n_percent = []
        self.cpu_time_prelim_box = []
        self.cpu_time_fraction_events = []
        self.cpu_time_add_events = []
        self.cpu_time_redistribute_data = []
        self.cpu_time_split = []
        self.cpu_time_meta_data = []
        self.cpu_time_total = []

        self.wall_time_n_percent = []
        self.wall_time_prelim_box = []
        self.wall_time_fraction_events = []
        self.wall_time_add_events = []
        self.wall_time_redistribute_data = []
        self.wall_time_split = []
        self.wall_time_meta_data = []
        self.wall_time_total = []

        self.number_events = []

    def evaluate(self):
        # 1. Get all names of all data files and sort them
        info = self.get_file_information()

        # 2. Read in the data for each file
        self.read_in_data(info)

        # 3. Plot the entire data set
        self.plot()

    def plot(self):
        plt.close('all')
        f, axarr = plt.subplots(5, 2, sharex=True)

        self.setup_error_plot(axarr, 0, 0, self.wall_time_total, 'ro', "Num Ranks", "Total wall time")
        self.setup_error_plot(axarr, 0, 1, self.number_events, 'ro', "Num Ranks", "Num Events per rank")
        self.setup_error_plot(axarr, 1, 0, self.wall_time_n_percent, 'ro', "Num Ranks", "N percent (w.t.)")
        self.setup_error_plot(axarr, 1, 1, self.wall_time_prelim_box, 'ro', "Num Ranks", "Prelim box (w.t.)")
        self.setup_error_plot(axarr, 2, 0, self.wall_time_fraction_events, 'ro', "Num Ranks", "Fraction events (w.t.)")
        self.setup_error_plot(axarr, 2, 1, self.wall_time_add_events, 'ro', "Num Ranks", "Add events(w.t.)")
        self.setup_error_plot(axarr, 3, 0, self.wall_time_redistribute_data, 'ro', "Num Ranks", "Redistribute data (w.t.)")
        self.setup_error_plot(axarr, 3, 1, self.wall_time_split, 'ro', "Num Ranks", "Split (w.t.)")
        self.setup_error_plot(axarr, 4, 0, self.wall_time_meta_data, 'ro', "Num Ranks", "Meta data (w.t.)")

        plt.show()

    def setup_error_plot(self, axarr, row, column, data, color, xlabel, ylabel):
        axis = axarr[row, column]
        mean = [element.mean for element in data]
        std = [element.std for element in data]
        ranks = [element.number_of_ranks for element in data]

        axis.errorbar(ranks, mean, std, fmt=color)
        axis.set_xlabel(xlabel)
        axis.set_ylabel(ylabel)
        axis.set_xscale('log', nonposx='clip')
        axis.set_yscale('log', nonposy='clip')

    def read_in_data(self, info):
        for element in info:
            cpu_time_n_percent = []
            cpu_time_prelim_box = []
            cpu_time_fraction_events = []
            cpu_time_add_events = []
            cpu_time_redistribute_data = []
            cpu_time_split = []
            cpu_time_meta_data = []
            cpu_time_total = []

            wall_time_n_percent = []
            wall_time_prelim_box = []
            wall_time_fraction_events = []
            wall_time_add_events = []
            wall_time_redistribute_data = []
            wall_time_split = []
            wall_time_meta_data = []
            wall_time_total = []
            number_events = []

            number_of_ranks = element.number_of_ranks
            path = element.file_name
            with open(path, 'r') as f:
                for index in range(0, number_of_ranks):
                    self.read_time_line(f, cpu_time_n_percent, wall_time_n_percent)
                    self.read_time_line(f, cpu_time_prelim_box, wall_time_prelim_box)
                    self.read_time_line(f, cpu_time_fraction_events, wall_time_fraction_events)
                    self.read_time_line(f, cpu_time_add_events, wall_time_add_events)
                    self.read_time_line(f, cpu_time_redistribute_data, wall_time_redistribute_data)
                    self.read_time_line(f, cpu_time_split, wall_time_split)
                    self.read_time_line(f, cpu_time_meta_data, wall_time_meta_data)
                    self.read_time_line(f, cpu_time_total, wall_time_total)

                self.read_number_events(f, number_events)

            # Now generate the mean and std and add to data information
            self.add_data(cpu_time_n_percent, self.cpu_time_n_percent, number_of_ranks)
            self.add_data(cpu_time_prelim_box, self.cpu_time_prelim_box, number_of_ranks)
            self.add_data(cpu_time_fraction_events, self.cpu_time_fraction_events, number_of_ranks)
            self.add_data(cpu_time_add_events, self.cpu_time_add_events, number_of_ranks)
            self.add_data(cpu_time_redistribute_data, self.cpu_time_redistribute_data, number_of_ranks)
            self.add_data(cpu_time_split, self.cpu_time_split, number_of_ranks)
            self.add_data(cpu_time_meta_data, self.cpu_time_meta_data, number_of_ranks)
            self.add_data(cpu_time_total, self.cpu_time_total, number_of_ranks)

            self.add_data(wall_time_n_percent, self.wall_time_n_percent, number_of_ranks)
            self.add_data(wall_time_prelim_box, self.wall_time_prelim_box, number_of_ranks)
            self.add_data(wall_time_fraction_events, self.wall_time_fraction_events, number_of_ranks)
            self.add_data(wall_time_add_events, self.wall_time_add_events, number_of_ranks)
            self.add_data(wall_time_redistribute_data, self.wall_time_redistribute_data, number_of_ranks)
            self.add_data(wall_time_split, self.wall_time_split, number_of_ranks)
            self.add_data(wall_time_meta_data, self.wall_time_meta_data, number_of_ranks)
            self.add_data(wall_time_total, self.wall_time_total, number_of_ranks)

            self.add_data(number_events, self.number_events, number_of_ranks)

    @staticmethod
    def add_data(data, location_to_add, number_of_ranks):
        mean = np.mean(data)
        std = np.std(data)
        location_to_add.append(measurement(number_of_ranks=number_of_ranks, mean=mean, std=std, raw=data))

    @staticmethod
    def read_time_line(file_handle, cpu_time_container, wall_time_container):
        line = file_handle.readline()
        line = "".join(line.split())
        cpu_time, wall_time = line.split(",")
        cpu_time_container.append(float(cpu_time))
        wall_time_container.append(float(wall_time))

    @staticmethod
    def read_number_events(file_handle, number_events_container):
        line = file_handle.readline()
        line = "".join(line.split())
        events = line.split(",")

        container = []
        for e in events:
            container.append(int(e))
        number_events_container.append(container)

    def get_file_information(self):
        info = []
        files = os.listdir(self.path_to_data)
        files = [os.path.join(self.path_to_data, file) for file in files]
        for file in files:
            tmp = file.split(".")
            val = tmp[0].split("_")
            ranks = int(val[-1])
            info.append(file_information(number_of_ranks=ranks, file_name=file))

        # Sort by number of ranks
        info = sorted(info, key=lambda f_info: f_info.number_of_ranks)
        return info


### 800MB file
path = os.path.join(os.getcwd(), "measurement_TOPAZ_3132_event_10x/")

### 8 GB file (~2e9 events)
# path = os.path.join(os.getcwd(), "measurement_TOPAZ_3132_event_100x/")

### 40GB file (1e10 events)
# path = os.path.join(os.getcwd(), "measurement_TOPAZ_3132_event_500x/")

evaluator = Evaluate(path)
evaluator.evaluate()