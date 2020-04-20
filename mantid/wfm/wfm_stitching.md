# Stitching wave-frame multiplication data at ESS

## Introduction



## Method 1: Using peak-finding

### Step by step procedure description

The procedure employed to find the WFM frames in the recorded data is the following.

1. The neutron counts from all pixels are histogrammed into a single spectrum, giving the characteristic bumped spectrum, shown as a black curve in Fig. 1 (left).
1. The spectrum is then smoothed using a [Gaussian filter](https://docs.scipy.org/doc/scipy/reference/generated/scipy.ndimage.gaussian_filter1d.html) using a standard deviation of 2 (grey curve).
1. The background estimation is carried out by histogramming the neutron counts in number-of-occurence bins, to find the most common count in the data. This will almost always be the background, which show a high occurence of very low counts, as can be seen in Fig. 1 (red dashed line in the right panel).
1. This raw background value is modified in a conservative way by adding to it 5% of the range between the raw background amplitude and the maximum amplitude in the data. This updated background value is represented by the pink dashed line in the right panel.
1. The leading (left) edge of the signal is then found by iterating through the spectrum, starting from the left hand side and finding the first data point that exceeds the updated background value. This edge is marked by a blue dot in the left panel. The same is repeated for the trailing edge (yellow dot), starting from the right hand side and iterating towards the left.
1. We then need to find 5 valleys (or inverted peaks) between these two edges. A [peak-finding](https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.find_peaks.html) algorithm is called on the inverted data (to find the valleys). The `prominence` parameter is given a value of `0.05 * (signal_maximum - signal_minimum)`. The 5 valleys are marked with red dots in the left panel.
1. Once the 5 valleys, and hence the 6 frames, are found, we compute the mean amplitude inside each frame. These are represented by the green horizontal lines.
1. The inter-frame gaps are cut out by defining a frame edge as the first value, starting from the centre of a given valley, that exceeds 30% of the frame average (brown horizontal lines). The frame edges are found by starting from each of the five red dots and navigating through the spectrum towards first the left, to find the previous frame's upper bound, and then the right, to find the next frame's lower bound.
1. The leading (blue dot) and trailing (yellow dot) edges complete the set of frame boundaries.

![peak-finding](peak_finding.png)

## Method 2: Using TOF diagrams in a post-processing step
