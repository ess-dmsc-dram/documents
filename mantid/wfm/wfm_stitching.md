# Stitching wave-frame multiplication data at ESS

## Introduction



## Method 1: Using peak-finding

### Description of the frame-edge detection procedure

The procedure employed to find the WFM frames in the recorded data is the following.

1. The neutron counts from all pixels are histogrammed into a single spectrum, giving the characteristic bumped spectrum, shown as a black curve in Fig. 1 (left).
1. The spectrum is then smoothed using a [Gaussian filter](https://docs.scipy.org/doc/scipy/reference/generated/scipy.ndimage.gaussian_filter1d.html) using a standard deviation of 2 (grey curve).
1. The background estimation is carried out by histogramming the neutron counts in number-of-occurence bins, to find the most common count in the data. This will almost always be the background, which show a high occurence of very low counts, as can be seen in Fig. 1 (red dashed line in the right panel).
1. This raw background value is modified in a conservative way by adding to it 5% of the range between the raw background amplitude and the maximum amplitude in the data. This updated background value is represented by the pink dashed line in the right panel.
1. The leading (left) edge of the signal is then found by iterating through the spectrum, starting from the left hand side and finding the first data point that exceeds the updated background value. This edge is marked by a blue dot in the left panel. The same is repeated for the trailing edge (yellow dot), starting from the right hand side and iterating towards the left.
1. We then need to find 5 valleys (or inverted peaks) between these two edges. A [peak-finding](https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.find_peaks.html) algorithm from the Scipy library is called on the inverted data (to find the valleys). The `prominence` parameter is given a value of `0.05 * (signal_maximum - signal_minimum)`. The 5 valleys are marked with red dots in the left panel.
1. Once the 5 valleys, and hence the 6 frames, are found, we compute the mean amplitude inside each frame. These are represented by the green horizontal lines.
1. The inter-frame gaps are cut out by defining a frame edge as the first value, starting from the centre of a given valley, that exceeds 30% of the frame average (brown horizontal lines). The frame edges are found by starting from each of the five red dots and navigating through the spectrum towards first the left, to find the previous frame's upper bound, and then the right, to find the next frame's lower bound.
1. The leading (blue dot) and trailing (yellow dot) edges complete the set of frame boundaries.

![peak-finding](peak_finding.png)
**Figure 1:** Left: raw data from a diffraction experiment at V20, showing the 6 WFM frames in different colours, as well as various markers that illustrate the steps in the frame finding algorithm (see text). Right: Histogramming of counts in amplitude bins to detect the background as the most common count occurence.

### Applying the conversion to time-of-flight

Because WFM is essentially making 6 new pulses from a single long pulse, the position of the neutron source (or source chopper in the case of V20) is considered to be half-way between the two WFM choppers. In order to conserve the wavelength of the neutrons, the data needs to be converted  from 'Arrival time at detector' to real 'Time-of-flight'.

Each frame needs to be shifted by a different value, as described in [Woracek et al. (2016)](https://doi.org/10.1016/j.nima.2016.09.034). This article also outlines the method used to compute the different frame shifts, and this will thus not be repeated here. We simply list the numbers by which the frames were shifted:

| Frame number | 1 | 2 | 3 | 4 | 5 | 6 |
| Tof shift [&mu;s] | -6630 | -9050 | -11303 | -13398 | -15344 | -17154 |

As explained in Woracek et al. (2016), the shifts for frames 2-6 are computed from the WFM chopper cut-out angles and rotation frequency, but depend on a initial frame shift for the first frame, which is free parameter. The value of the first frame shift (given in the table), was computed by fitting a Bragg edge to the WFM signal from an iron plate, using the same expenrimental set-up.

Figure 2 shows an example of neutron scattering data collected at V20 (Si sample), before (top) and after (bottom) stitching. Note that some artifacts (spikes) show up between some of the frames, due to signal overlap. However, these get corrected when the data is normalized by a monitor signal which shows identical artifacts.

![before-after](si_frames.png)
**Figure 2:** Before (top panel) and after (bottom panel) the stitching procedure.

### Short-comings of the peak-finding method



## Method 2: Using TOF diagrams in a post-processing step
