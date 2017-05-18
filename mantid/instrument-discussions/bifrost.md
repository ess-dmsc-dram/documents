# Bifrost

Meeting 2017-05-18

- Rasmus Toft-Petersen
- Simon Heybrock

## General

- User mid 2023 (among first 8 instruments)
- Hot commissioning 2022
- worst case 1e6 counts/s, mostly 10x lower than that
  - might actually be 1e7 before calibration in early hot commissioning, but could probably use attenuator

## Instrument

### Scans

- A4 = tank rotation (might be continuous scan but should be possible to approximate with step scan)
- A3 = sample scan

### Monitors

- scans -> need time resolved monitors
- no single shot, monitors integrated over intervals of seconds to minutes
- details still open

### Beam path

- path component approximation as prototyped for Mantid Instrument-2.0 should be fine
- current "fudging" should also be sufficient
- L1 might be wavelength dependent (will be simulated soon)!

## Event mode

- stroboscopic measurements

## MDWorkspace

S(Q,\omega) -> actually S(Q_1, Q_2, \omega)
- absolutely essential from day 1 of hot commissioning
  -> check what SofQw(MatrixWorkspace) does in Mantid - is that just |Q|?
- up to 5 Giga bins (uniform binning)
- need to see results within time scale of (seconds to) minutes

## "Continuous angle multiple analsysis"

- no RRM via choppers (unlike other spectrometers at ESS)
- several different analyzers in series -> different E_f
- could mostly be analyzed separately, but would alo need to be able to do comparisons, etc.
- for live mode, it might be sufficient to reduce data only from a single analyzer arc, in case that is necessary for performance

## InstrumentView

- 5000 pixels -> no performance issue with current implementation

## Calibration and sample alignment

- Group all pixels (3 tubes, or just central) hit by same analyzer
- Plot I(\lambda, A3) -> sample alignment
- might be possible to do this "offline", if done in short intervals (few minutes) and provided that it is automizable
- white beam, close slits until bragg peak goes darker (reduce background), should be automatizable
  - using attenuation to reduce flux
- vanadium runs -> normalization file (monthly basis)
- detector safety system: bragg peak too strong -> detector will ramp down voltage -> disables detector
  - mask detectors (automatically)
  - notify user in NICOS?
- Rasmus will look into what is needed as toolbox for alignment and calibration
- Spurions
  - need masking
  - masking in (Q,\omega), does Mantid support that? Need to at least compare there -> get detector space / time bins for masking from (Q,\omega)
- normalization for detectors and for analysis (actually combined)
