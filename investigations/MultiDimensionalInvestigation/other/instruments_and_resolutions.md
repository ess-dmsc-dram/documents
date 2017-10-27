# T-REX

T-REX is a time-of-floght, reciprocal space explorer which can also perform
magnetism-sensitive measurments. They measure a 4D reciprocal space (assume Q and E).

The specs for this instrument are:

| Quantity          | Range                 |
|-------------------|-----------------------|
| Q range           | 0.05 A^-1 to 17 A^-1  |
| Q resolution      | 0.01 A^-1 to 0.1 A^-1 |
| incid. energy     | 2 meV to 160 meV      |
| energy resolution | 20uEV to 10meV        |

#### Parameter space cell count

###### Linear resolution case
Assumption: Q range refers to the modulus, ie we are dealing with a hyphershell
            which ranges from q_range_min to q_range_max and e_min to e_max.

The volume of the Q component is: $\frac{4}{3}\pi\left( 17^{3} - 0.05^{3} \rigth) \AA^{-3} \approx 20600\AA^{-3}$

For the momentum tranfer component of the parameter space will lead to a range of $20600/ (0.01)^{3} = 2e10$ to $20600/ (0.1)^{3}=2e7$ cells.

For the number of cells in the energy component of the parameter space lies between  
$(160 - 2)/0.02=7900$ and $(160 - 2)/10=15.8$

This range of possible cells that we can have is between 3.1e8 and 1.6e14.

This analysis is most likely flawed, but it shows that in the best case scenario
of ~1e8 we are dealing with data sizes of a couple of gigabytes and in the worst case scenario of ~1e14 we are dealing with data sizes of almost a petabyte. Assuming that each cell only needs to contain signal (int) and error(float), as
the possition can be easily infered from the regular grid.

The truth of this will lie more closely in the tens of GB case when logarithmic
binning is used as is the case for WISH.

# Esko

The Esko instrument is a time-of-flight diffractometer which is optimised for
small sample sizes. It has moving detectors. The wavelength range is $1.8 \AA$
to $3.55\AA$ with a wavelength resolution of $4%$ at the lower end and $2%$ at the
upper end of that range. The detector geometry is not specified in the document,
since it is variable. Some configurations for the geometry are:

|----------------|------------------------------|
| Distance       |  Angle in horizontal plane   |
|----------------|------------------------------|
|  20cm          |  330 degrees                 |
|  30cm          |  270 degrees                 |
|  50cm          |  186 degrees                 |
|  100cm         |  100 degrees                 |
|----------------|------------------------------|

with a pixel size of 0.2mm and a detector size of 60cmx60cm. This should allow
us to estimate the angle resolution and the available detector space.

###### 100cm scenario

In the horizontal plane the angles range from -50 to +50 degrees. In the vertical
plane the angle is $\atan \frac{30/100} \approx 17^{\circ}$. For an upper bound
estimate we get a value of about $Q\approx 5.4\AA^{-1}$ (for min wavelength and max angle).
Note that we just used $Q=2*k*\sin\left(2\theta\right)$
As a volume we assume a sphere, hence we estimate it to be $624\\A^{-3}$. There is no
engergy dimension that we need to consider.

We estimate the resolution of theta to be $\atan\left(0.2\times 10^{-3}\right) \approx 0.01[^{\circ}]$
and the wavelength is about $0.07\AA$. With this we can propagte the uncertainty to Q.
We obtain a Q resolution of about in the range from $9e-4\AA^{-1}$ to $2e-1\AA^{-1}$. This
leads to resolution cubes of $7e-10\AA^{-3}$ and $8e-3\AA^{-3}$.

Finally we get an estimate of the parameter cell count between $8e4$ and $9e11$. This leads
to an estimated memory usage between several megabyte and low ten(s) of terabyte.

This extremly wide estimate suffers most likely from the fact that we have a variable
resolution in Q which is hard to take into account without having exact parameters
for a specific scenarios from the instrument scientists.


# MAGIC

MAGIC provides polarized neutron time-of flight spectroscopy of small single crystals. From the documents it is not clear what the resolutions will be.


# WISH COMPARISON

TODO
