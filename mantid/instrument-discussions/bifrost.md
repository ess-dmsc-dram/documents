# Bifrost

Meeting 2017-05-18

- Rasmus Toft-Petersen
- Simon Heybrock

## General

- User mid 2023 (among first 8 instruments)
- Hot commissioning 2022

- normalization for detectors and for analysis (actually combined)

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

S(Q,\omega) -> actually S(Q_1, Q_2, \omega) (absolutely essential from day 1 of hot commissioning)
  -> check what SofQw does in Mantid
time scale seconds to minutes

up to 5 GigaBins



## "Continuous angle multiple analsysis"

- no RRM via choppers (unlike other spectrometers at ESS)
- several different analyzers in series -> different E_f
- might be analyzed separately, but would alo need to be able to do comparisons, etc.
- for live mode, it might be sufficient to reduce data only from a single analyzer arc, in case that is necessary for performance

## InstrumentView

- 5000 pixels -> no performance issue with current implementation

## Sample alignment / Calibration

- Group all pixels (3 tubes, or just central) hit by same analyzer
- Plot I(\lambda, A3) -> sample alignment
- might be possible to do this offline, if done in short intervals (few minutes)

- white beam, close slits until bragg peak goes darker (reduce background), should be automatizable
  - using attenuation to reduce flux

- vanadium runs -> normalization file (monthly basis)


- detector safety system: bragg peak too strong -> detector will ramp down voltage -> disables detector
  - mask detectors
  - notify user in NICOS?


- worst case 1e6 counts/s, mostly 10x
  - might actually be 1e7 before calibration in early hot commissioning (might use attenuator)

- will look into what is needed as toolbox for alignment and calibration


- Spurions
  - need masking
  - masking in (Q,\omega)? (at least compare there?) -> get detector space / time bins
