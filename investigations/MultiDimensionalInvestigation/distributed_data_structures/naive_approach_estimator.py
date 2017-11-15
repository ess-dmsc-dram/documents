import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.axes3d import Axes3D
from matplotlib import cm


class BalancedKaryTreeEstimator(object):
    """ This estimator assumes that the tree is balanced"""
    def __init__(self, split_into, max_events_in_box):
        self._split_into = split_into
        self._max_event_in_box = max_events_in_box

    def number_of_leaf_nodes(self, number_events):
        height = self._get_height(number_events)
        return pow(self._split_into, height)

    def number_of_inner_nodes(self, number_events):
        total_nodes = self.number_of_total_nodes(number_events)
        leaf_nodes = self.number_of_leaf_nodes(number_events)
        return total_nodes - leaf_nodes

    def number_of_total_nodes(self, number_events):
        height = self._get_height(number_events)
        return (1-pow(self._split_into, height+1))/(1 - self._split_into)

    def _get_height(self, number_of_events):
        numerator = np.log(number_of_events/self._max_event_in_box)
        denominator = np.log(self._split_into)
        division = numerator/denominator
        return np.ceil(division)

    def plot_total_number_nodes(self, start, stop):
        num_events = np.logspace(start, stop)
        total_nodes = self.number_of_total_nodes(num_events)
        plt.plot(num_events, total_nodes, 'o')
        plt.xscale("log")
        plt.yscale("log")
        plt.show()

    def _get_3d_data(self, total_nodes, max_ranks, num_events):
        ranks = np.arange(1, max_ranks+1, 1)
        ratios = []
        for rank in ranks:
            total_nodes_per_rank = self.number_of_total_nodes(num_events/rank)
            ratio = total_nodes/total_nodes_per_rank
            ratios.append(ratio)
        stacked_ratios = np.vstack(ratios)

        # Generate the meshgrid
        x, y = np.meshgrid(num_events, ranks)

        return x, y, stacked_ratios

    def plot_scaling(self, start, stop, max_ranks):
        num_events = np.logspace(start, stop, num=50)
        total_nodes = self.number_of_total_nodes(num_events)

        # for ranks in range(1, max_ranks + 1, 5):
        total_nodes_per_rank = self.number_of_total_nodes(num_events/max_ranks)
        ratio = total_nodes/total_nodes_per_rank

        # Get the data for the 3D plot. We want ranks vs events vs scale
        x, y, data = self._get_3d_data(total_nodes, max_ranks, num_events)

        # Start plotting
        fig = plt.figure(figsize=plt.figaspect(0.5))

        # -----------------
        # Plot 1
        # -----------------
        raw_axis = fig.add_subplot(2, 2, 1)
        raw_axis.loglog(num_events, total_nodes, 'r')
        raw_axis.loglog(num_events, total_nodes_per_rank, 'b')
        raw_axis.set_xlabel("Number of events")
        raw_axis.set_ylabel("Total boxes ({} nodes)".format(max_ranks))
        raw_axis.legend(["Serial", "Parallel (per node)"])

        # -----------------
        # Plot 2
        # -----------------
        scale_axis = fig.add_subplot(2, 2, 2)
        scale_axis.semilogx(num_events, ratio, 'r')
        scale_axis.set_xlabel("Number of events")
        scale_axis.set_ylabel("Scale ({} nodes)".format(max_ranks))

        # ------
        # Plot 3
        # ------
        ax = fig.add_subplot(2, 2, 3, projection='3d')
        ax.set_xlabel("Events")
        ax.set_ylabel("Ranks")
        ax.set_zlabel("Scale")

        surf = ax.plot_surface(x, y, data, rstride=1, cstride=1, cmap=cm.coolwarm,
                               linewidth=0, antialiased=False)
        fig.colorbar(surf, shrink=0.5, aspect=10)
        plt.show()


SPLIT_INTO = 125
MAX_EVENTS_PER_BOX = 1000
NUMBER_OF_MACHINES = 30

estimator = BalancedKaryTreeEstimator(split_into=SPLIT_INTO, max_events_in_box=MAX_EVENTS_PER_BOX)
estimator.plot_scaling(6, 12, NUMBER_OF_MACHINES)
