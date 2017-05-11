# Diffraction

Meeting 2017-05-11
- Werner Schweika
- Simon Heybrock

## General

- Powder diffraction and single crystal instruments may be used for both techniques
- Have a look at `qevis` by Florian Rhiem (visualization of MD event data)
- Marina is doing related relevant work for POWGEN (projection, 2D Rietveld) in Mantid

## Instrument View

- Day 1: Does not need to present 3D detector volume, projection towards sample position onto 2D plane sufficient

## Event Mode

- Filtering
- Single crystal extinction correction:
  - I(h,k,l, lambda) and filter out data points in lambda that are influenced by absorption
  - Could be 4D workspace Qx, Qy, Qz, lambda? Or can this simply be I(h,k,l, lambda)?
  - It is not clear that we need events for this?
  
## Monitors

- Event mode
- Efficiency 1e-5 to 1e-3 relative to incident of max. 1e9
- Need time resolution, high-rate experiments typically short
- Shortest time scale might be pulsed magnet (50 ms pulse, with time variation)
  
## Instrument

- No moving detectors, apart from NMX
- Map 3D detectors to 2D, but *not* onto binning "defined" by the surface voxels, need finer resolution
- 3D detectors aligned such that effictive resolution mapped to 2D is smaller than pixel size
  - For powder diffraction, as far as I understand, we simply do not map onto 2D -- just use existing diffraction focussing algorithms?
  - For single crystal, where is this relevant? Just go into MDWorkspace?

## MDWorkspace

- Heavily used for single crystal.

## Bringup:

- Live instrument view
- Python scripts
- Live reduction:
  - Powder: 1D and 2D live view
  - Single crystal: Q-space display and HKL lists do not need to be live
    
## Future

- Filter out scattering from anything but the sample, using trajectories seen in 3D detectors
